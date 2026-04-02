// interperter.c - I am not sure if I need this file

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

/* Token Types for Psyche-set Language */
typedef enum {
    TOKEN_PRINT, TOKEN_EXIT, TOKEN_INPUT, TOKEN_LEN, TOKEN_TYPE,
    TOKEN_STR_CAST, TOKEN_INT_CAST, TOKEN_FLOAT_CAST, TOKEN_BOOL_CAST,
    TOKEN_LIST_CAST, TOKEN_DICT_CAST, TOKEN_SET_CAST, TOKEN_TUPLE_CAST, TOKEN_RANGE,
    TOKEN_IF, TOKEN_ELSE, TOKEN_BUT, TOKEN_BUT_IF, TOKEN_CHANGE,
    TOKEN_AND, TOKEN_OR, TOKEN_NOT,
    TOKEN_GT, TOKEN_LT, TOKEN_GE, TOKEN_LE, TOKEN_EQ, TOKEN_NE,
    TOKEN_CLASS, TOKEN_FUNCTION, TOKEN_METHOD, TOKEN_INTERNALIZE, TOKEN_RETURN, TOKEN_SELF,
    TOKEN_ADD, TOKEN_SUB, TOKEN_MUL, TOKEN_DIV,
    TOKEN_ADD_ASSIGN, TOKEN_SUB_ASSIGN, TOKEN_MUL_ASSIGN, TOKEN_DIV_ASSIGN,
    TOKEN_F_DIV, TOKEN_MOD, TOKEN_POW, TOKEN_DOESNT_EXIST,
    TOKEN_CONST, TOKEN_INT_TYPE, TOKEN_FLOAT_TYPE, TOKEN_STR_TYPE, TOKEN_BOOL_TYPE,
    TOKEN_LIST_TYPE, TOKEN_DICT_TYPE, TOKEN_SET_TYPE, TOKEN_TUPLE_TYPE,
    TOKEN_IS, TOKEN_IS_NO, TOKEN_LIKE,
    TOKEN_FOR, TOKEN_STOP, TOKEN_WHILE, TOKEN_TRUE, TOKEN_SKIP, TOKEN_LOOP, TOKEN_UNTIL,
    TOKEN_NOTE, TOKEN_TAG, TOKEN_IDENTIFIER, TOKEN_STRING, TOKEN_NUMBER
} TokenType;

/* Keyword Mapping Structure */
typedef struct {
    char* keyword;
    TokenType type;
} Keyword;

Keyword keywords[] = {
    {"print", TOKEN_PRINT}, {"exit", TOKEN_EXIT}, {"input", TOKEN_INPUT},
    {"len", TOKEN_LEN}, {"type", TOKEN_TYPE}, {"str", TOKEN_STR_CAST},
    {"int", TOKEN_INT_CAST}, {"float", TOKEN_FLOAT_CAST}, {"bool", TOKEN_BOOL_CAST},
    {"list", TOKEN_LIST_CAST}, {"dict", TOKEN_DICT_CAST},
    {"set", TOKEN_SET_CAST}, {"tuple", TOKEN_TUPLE_CAST}, {"range", TOKEN_RANGE},
    {"if", TOKEN_IF}, {"else", TOKEN_ELSE}, {"but", TOKEN_BUT}, {"but_if", TOKEN_BUT_IF}, {"change", TOKEN_CHANGE},
    {"and", TOKEN_AND}, {"or", TOKEN_OR}, {"not", TOKEN_NOT},
    {"gt", TOKEN_GT}, {"lt", TOKEN_LT}, {"ge", TOKEN_GE}, {"le", TOKEN_LE}, {"eq", TOKEN_EQ}, {"ne", TOKEN_NE},
    {"class", TOKEN_CLASS}, {"function", TOKEN_FUNCTION}, {"method", TOKEN_METHOD}, {"internalize", TOKEN_INTERNALIZE}, {"return", TOKEN_RETURN}, {"self", TOKEN_SELF},
    {"+", TOKEN_ADD}, {"-", TOKEN_SUB}, {"*", TOKEN_MUL}, {"/", TOKEN_DIV},
    {"+=", TOKEN_ADD_ASSIGN}, {"-=", TOKEN_SUB_ASSIGN}, {"*=", TOKEN_MUL_ASSIGN}, {"/=", TOKEN_DIV_ASSIGN},
    {"//", TOKEN_F_DIV}, {"%", TOKEN_MOD}, {"**", TOKEN_POW}, {"doesnt_exist", TOKEN_DOESNT_EXIST},
    {"const", TOKEN_CONST}, {"int", TOKEN_INT_TYPE}, {"float", TOKEN_FLOAT_TYPE}, {"str", TOKEN_STR_TYPE}, {"bool", TOKEN_BOOL_TYPE},
    {"list", TOKEN_LIST_TYPE}, {"dict", TOKEN_DICT_TYPE}, {"set", TOKEN_SET_TYPE}, {"tuple", TOKEN_TUPLE_TYPE},
    {"is", TOKEN_IS}, {"is_no", TOKEN_IS_NO}, {"like", TOKEN_LIKE},
    {"for", TOKEN_FOR}, {"stop", TOKEN_STOP}, {"while", TOKEN_WHILE}, {"true", TOKEN_TRUE}, {"skip", TOKEN_SKIP}, {"loop", TOKEN_LOOP}, {"until", TOKEN_UNTIL},
    {"note", TOKEN_NOTE}, {"tag", TOKEN_TAG}, {"identifier", TOKEN_IDENTIFIER}, {"string", TOKEN_STRING}, {"number", TOKEN_NUMBER}
};