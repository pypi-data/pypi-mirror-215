from pyspark.sql.functions import array, lit, struct
from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *



def typed_lit(obj):
    if isinstance(obj, list):
        return array([typed_lit(x) for x in obj])
    elif isinstance(obj, dict):
        elementsList = []
        for key, value in obj.items():
            elementsList.append(typed_lit(value).alias(key))
        return struct(elementsList)
    else:
        try:
            # int, float, string
            return lit(obj)
        except:
            # class type
            return typed_lit(obj.__dict__)


def has_column(df, col):
    try:
        df[col]
        return True
    except:
        return False


def createScalaList(spark, l):
    return spark.sparkContext._jvm.PythonUtils.toList(l)


def createScalaColumnList(spark, cols):
    return spark.sparkContext._jvm.PythonUtils.toList([item._jc for item in list(cols)])


def createScalaMap(spark, dict):
    return spark.sparkContext._jvm.PythonUtils.toScalaMap(dict)


def createScalaColumnMap(spark, dict):
    jcolDict = {k: col._jc for k, col in dict.items()}
    return spark.sparkContext._jvm.PythonUtils.toScalaMap(jcolDict)


def createScalaColumnOption(spark, value):
    if value is None:
        return spark.sparkContext._jvm.scala.Option.apply(None)
    else:
        return spark.sparkContext._jvm.scala.Some(value._jc)


def createScalaOption(spark, value):
    if value is None:
        return spark.sparkContext._jvm.scala.Option.apply(None)
    else:
        return spark.sparkContext._jvm.scala.Some(value)


def unionAll(in0: DataFrame, in1: DataFrame, *inDFs: DataFrame):
    _inputs = [in0, in1]
    _inputs.extend(inDFs)
    res = []
    for v in _inputs:
        if v is not None:
            res.append(v)

    if len(res) == 1:
        result = res[0]
    else:
        result = res[0]
        rest = res[1:]
        for df in rest:
            result = result.unionAll(df)

    return result


def setOperation(inputs: list, op: str, allowMissingColumns: bool= False):
    res = []
    for v in inputs:
        if v is not None:
            res.append(v)

    if len(res) == 1:
        result = res[0]
    else:
        result = res[0]
        rest = res[1:]
        for df in rest:
            if op == "unionAll":
                result = result.unionAll(df)
            elif op =="intersectAll":
                result = result.intersectAll(df)
            elif op =="exceptAll":
                result = result.exceptAll(df)
            elif op =="unionByName":
                if allowMissingColumns is None:
                    result = result.unionByName(df, allowMissingColumns)
                else:
                    result = result.unionByName(df)


    return result

def unionAll(in0: DataFrame, in1: DataFrame, *inDFs: DataFrame) -> DataFrame:
    _inputs = [in0, in1]
    _inputs.extend(inDFs)
    return setOperation(_inputs, "unionAll")


def intersectAll(in0: DataFrame, in1: DataFrame, *inDFs: DataFrame) -> DataFrame:
    _inputs = [in0, in1]
    _inputs.extend(inDFs)
    return setOperation(_inputs, "intersectAll")

def exceptAll(in0: DataFrame, in1: DataFrame, *inDFs: DataFrame) -> DataFrame:
    _inputs = [in0, in1]
    _inputs.extend(inDFs)
    return setOperation(_inputs, "exceptAll")


def unionByName(in0: DataFrame, in1: DataFrame, *inDFs: DataFrame, allowMissingColumns: bool = False) -> DataFrame:
    _inputs = [in0, in1]
    _inputs.extend(inDFs)
    return setOperation(_inputs, "unionByName", allowMissingColumns)
