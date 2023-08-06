# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE
import awkward as ak
from awkward._behavior import behavior_of
from awkward._layout import wrap_layout
from awkward._nplikes import ufuncs
from awkward._nplikes.numpylike import NumpyMetadata
from awkward.highlevel import Array

np = NumpyMetadata.instance()


class ByteBehavior(Array):
    __name__ = "Array"

    def __bytes__(self):
        tmp = self.layout.backend.nplike.asarray(self.layout)
        if hasattr(tmp, "tobytes"):
            return tmp.tobytes()
        else:
            return tmp.tostring()

    def __str__(self):
        return str(self.__bytes__())

    def __repr__(self):
        return repr(self.__bytes__())

    def __iter__(self):
        yield from self.__bytes__()

    def __eq__(self, other):
        if isinstance(other, (bytes, ByteBehavior)):
            return bytes(self) == bytes(other)
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(self, other)

    def __add__(self, other):
        if isinstance(other, (bytes, ByteBehavior)):
            return bytes(self) + bytes(other)
        else:
            raise TypeError("can only concatenate bytes to bytes")

    def __radd__(self, other):
        if isinstance(other, (bytes, ByteBehavior)):
            return bytes(other) + bytes(self)
        else:
            raise TypeError("can only concatenate bytes to bytes")


class CharBehavior(Array):
    __name__ = "Array"

    def __bytes__(self):
        tmp = self.layout.backend.nplike.asarray(self.layout)
        if hasattr(tmp, "tobytes"):
            return tmp.tobytes()
        else:
            return tmp.tostring()

    def __str__(self):
        return self.__bytes__().decode("utf-8", "surrogateescape")

    def __repr__(self):
        return repr(self.__bytes__().decode("utf-8", "surrogateescape"))

    def __iter__(self):
        yield from self.__str__()

    def __eq__(self, other):
        if isinstance(other, (str, CharBehavior)):
            return str(self) == str(other)
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        if isinstance(other, (str, CharBehavior)):
            return str(self) + str(other)
        else:
            raise TypeError("can only concatenate str to str")

    def __radd__(self, other):
        if isinstance(other, (str, CharBehavior)):
            return str(other) + str(self)
        else:
            raise TypeError("can only concatenate str to str")


class ByteStringBehavior(Array):
    __name__ = "Array"

    def __iter__(self):
        for x in super().__iter__():
            yield x.__bytes__()


class StringBehavior(Array):
    __name__ = "Array"

    def __iter__(self):
        for x in super().__iter__():
            yield x.__str__()


def _string_equal(one, two):
    behavior = behavior_of(one, two)

    one, two = (
        ak.operations.without_parameters(one).layout,
        ak.operations.without_parameters(two).layout,
    )
    nplike = one.backend.nplike

    # first condition: string lengths must be the same
    counts1 = nplike.asarray(
        ak._do.reduce(one, ak._reducers.Count(), axis=-1, mask=False)
    )
    counts2 = nplike.asarray(
        ak._do.reduce(two, ak._reducers.Count(), axis=-1, mask=False)
    )

    out = counts1 == counts2

    # only compare characters in strings that are possibly equal (same length)
    possible = nplike.logical_and(out, counts1)
    possible_counts = counts1[possible]

    if len(possible_counts) > 0:
        onepossible = one[possible]
        twopossible = two[possible]

        reduced = ak.operations.all(
            ak.Array(onepossible) == ak.Array(twopossible), axis=-1
        ).layout
        # update same-length strings with a verdict about their characters
        out[possible] = reduced.data

    return wrap_layout(ak.contents.NumpyArray(out), behavior)


def _string_notequal(one, two):
    return ~_string_equal(one, two)


def _string_numba_typer(viewtype):
    import numba

    if viewtype.type.parameters["__array__"] == "string":
        return numba.types.string
    else:
        return numba.cpython.charseq.bytes_type


def _string_numba_lower(
    context, builder, rettype, viewtype, viewval, viewproxy, attype, atval
):
    import llvmlite.ir
    import numba

    whichpos = ak._connect.numba.layout.posat(
        context, builder, viewproxy.pos, viewtype.type.CONTENT
    )
    nextpos = ak._connect.numba.layout.getat(
        context, builder, viewproxy.arrayptrs, whichpos
    )

    whichnextpos = ak._connect.numba.layout.posat(
        context, builder, nextpos, viewtype.type.contenttype.ARRAY
    )

    startspos = ak._connect.numba.layout.posat(
        context, builder, viewproxy.pos, viewtype.type.STARTS
    )
    startsptr = ak._connect.numba.layout.getat(
        context, builder, viewproxy.arrayptrs, startspos
    )
    startsarraypos = builder.add(viewproxy.start, atval)
    start = ak._connect.numba.layout.getat(
        context, builder, startsptr, startsarraypos, viewtype.type.indextype.dtype
    )

    stopspos = ak._connect.numba.layout.posat(
        context, builder, viewproxy.pos, viewtype.type.STOPS
    )
    stopsptr = ak._connect.numba.layout.getat(
        context, builder, viewproxy.arrayptrs, stopspos
    )
    stopsarraypos = builder.add(viewproxy.start, atval)
    stop = ak._connect.numba.layout.getat(
        context, builder, stopsptr, stopsarraypos, viewtype.type.indextype.dtype
    )

    baseptr = ak._connect.numba.layout.getat(
        context, builder, viewproxy.arrayptrs, whichnextpos
    )
    rawptr = builder.add(
        baseptr,
        ak._connect.numba.layout.castint(
            context, builder, viewtype.type.indextype.dtype, numba.intp, start
        ),
    )
    rawptr_cast = builder.inttoptr(
        rawptr,
        llvmlite.ir.PointerType(llvmlite.ir.IntType(numba.intp.bitwidth // 8)),
    )
    strsize = builder.sub(stop, start)
    strsize_cast = ak._connect.numba.layout.castint(
        context, builder, viewtype.type.indextype.dtype, numba.intp, strsize
    )

    pyapi = context.get_python_api(builder)
    gil = pyapi.gil_ensure()

    strptr = builder.bitcast(rawptr_cast, pyapi.cstring)

    if viewtype.type.parameters["__array__"] == "string":
        kind = context.get_constant(numba.types.int32, pyapi.py_unicode_1byte_kind)
        pystr = pyapi.string_from_kind_and_data(kind, strptr, strsize_cast)
    else:
        pystr = pyapi.bytes_from_string_and_size(strptr, strsize_cast)

    out = pyapi.to_native_value(rettype, pystr).value

    pyapi.decref(pystr)

    pyapi.gil_release(gil)

    return out


def _cast_bytes_or_str_to_string(string):
    return ak.to_layout([string])


def register(behavior):
    behavior["byte"] = ByteBehavior
    behavior["__typestr__", "byte"] = "byte"
    behavior["char"] = CharBehavior
    behavior["__typestr__", "char"] = "char"

    behavior["bytestring"] = ByteStringBehavior
    behavior["__typestr__", "bytestring"] = "bytes"
    behavior["string"] = StringBehavior
    behavior["__typestr__", "string"] = "string"

    behavior[ufuncs.equal, "bytestring", "bytestring"] = _string_equal
    behavior[ufuncs.equal, "string", "string"] = _string_equal
    behavior[ufuncs.not_equal, "bytestring", "bytestring"] = _string_notequal
    behavior[ufuncs.not_equal, "string", "string"] = _string_notequal

    behavior["__numba_typer__", "bytestring"] = _string_numba_typer
    behavior["__numba_lower__", "bytestring"] = _string_numba_lower
    behavior["__numba_typer__", "string"] = _string_numba_typer
    behavior["__numba_lower__", "string"] = _string_numba_lower

    behavior["__cast__", str] = _cast_bytes_or_str_to_string
    behavior["__cast__", bytes] = _cast_bytes_or_str_to_string
