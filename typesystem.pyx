from openmath import openmath as om

cdef

singular_ctors = {
        "bigint": 
        {
            "to_om": bigint_to_om,
            "to_sing": bigint_to_sing
        },

        "bigintmat":
        {
            "to_om": bigintmat_to_om,
            "to_sing": bigintmat_to_sing
        },

        "def":
        {
            "to_om": def_to_om,
            "to_sing": def_to_sing
        },

        "ideal":
        {
            "to_om": ideal_to_om,
            "to_sing": ideal_to_sing
        },

        "int":
        {
            "to_om": int_to_om,
            "to_sing": int_to_sing
        },

        "intmat":
        {
            "to_om": intmat_to_om,
            "to_sing": intmat_to_sing
        },

        "intvec":
        {
            "to_om": intvec_to_om,
            "to_sing": intvec_to_sing
        },

        "list":
        {
            "to_om": list_to_om,
            "to_sing": list_to_sing
        },

        "map":
        {
            "to_om": map_to_om,
            "to_sing": map_to_sing
        },

        "matrix":
        {
            "to_om": matrix_to_om,
            "to_sing": matrix_to_sing
        },

        "module":
        {
            "to_om": module_to_om,
            "to_sing": module_to_sing
        },

        "number":
        {
            "to_om": number_to_om,
            "to_sing": number_to_sing
        },

        "poly":
        {
            "to_om": poly_to_om,
            "to_sing": poly_to_sing
        },

        "proc":
        {
            "to_om": proc_to_om,
            "to_sing": proc_to_sing
        },

        "resolution":
        {
            "to_om": resolution_to_om,
            "to_sing": resolution_to_sing
        },

        "ring":
        {
            "to_om": ring_to_om,
            "to_sing": ring_to_sing
        },

        "string":
        {
            "to_om": string_to_om,
            "to_sing": string_to_sing
        },

        "vector":
        {
            "to_om": vector_to_om,
            "to_sing": vector_to_sing
        },

        "cone":
        {
            "to_om": cone_to_om,
            "to_sing": cone_to_sing
        },

        "fan":
        {
            "to_om": fan_to_om,
            "to_sing": fan_to_sing
        },

        "polytope":
        {
            "to_om": polytope_to_om,
            "to_sing": polytope_to_sing
        }
}
