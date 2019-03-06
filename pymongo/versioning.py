import bson
import datetime
import pytest
import pymongo
import pymongo.collection
import pymongo.errors


PyCollection = pymongo.collection.Collection


@pytest.fixture
def mg_collection():
    db = "test_doc_access"
    col_name = "col"

    client = pymongo.MongoClient('localhost', 27017)
    db = client[db]
    db.drop_collection(col_name)
    collection = db[col_name]
    return collection


def __insert_doc(document, *, coll):
    doc_id = coll.insert_one(document).inserted_id
    return doc_id


def test_new_document_for_each_version(mg_collection: PyCollection):
    """
    RECORD 1:
    {"_id" : ObjectId("5c7eff669586645d20ebd66d"),
     "v" : 1,
     "docId" : ObjectId("5c7eff669586645d20ebd66c"),
     "data" : {},
     "createAt" : ISODate("2019-03-05T22:59:50.723Z"), }
    RECORD 2:
    {"_id" : ObjectId("5c7eff669586645d20ebd66e"),
     "v" : 2,
     "docId" : ObjectId("5c7eff669586645d20ebd66c"),
     "data" : {},
     "createAt" : ISODate("2019-03-05T22:59:50.726Z"), }
    """

    mg_collection.create_index([("docId", pymongo.DESCENDING),
                                ("v", pymongo.DESCENDING)],
                               unique=True)
    glob_doc_id = bson.ObjectId()

    def get_document(v=0):
        return {"v": v, "docId": glob_doc_id, "data": {},
                "createAt": datetime.datetime.utcnow(), }

    doc = get_document(v=1)
    doc_id = __insert_doc(doc, coll=mg_collection)
    assert doc_id

    doc = get_document(v=2)
    doc_id = __insert_doc(doc, coll=mg_collection)
    assert doc_id

    cnt = mg_collection.count_documents(filter={})
    assert 2 == cnt, "Should be 2 documents"

    res = mg_collection.find_one({"docId": glob_doc_id}, sort=[("v", -1)])
    assert 2 == res['v'], "The latest version is '2'"

    # Since we have unique index based on docId and v fields
    # it is impossible to insert the same version into DB.
    # In case of the exception, the code should increment
    # the version and retry the insert.
    with pytest.raises(pymongo.errors.DuplicateKeyError):
        __insert_doc(doc, coll=mg_collection)


def test_embedded_versioning(mg_collection: PyCollection):
    """
    {"_id": ObjectId("5c7f03aa9586645ddf13ccd5"),
     "current": {"v": 2, "data": {"val": 123}},
     "hist": [{"v": 1, "data": {"val": 1}}],
     "createAt": ISODate("2019-03-05T22:59:50.726Z"), }
    """

    doc = {"current": {"v": 1, "data": {"val": 1}, },
           "hist": [],
           "createAt": datetime.datetime.utcnow(), }
    doc_id = __insert_doc(doc, coll=mg_collection)
    assert doc_id

    result = mg_collection.update_one({"_id": doc_id}, {
        "$addToSet": {"hist": doc['current'], },
        "$set": {"current": {"v": 2, "data": {"val": 123}, }, }
    }, upsert=False)

    assert 1 == result.matched_count
    assert 1 == result.modified_count

    result = mg_collection.count_documents({"_id": doc_id})
    assert 1 == result
