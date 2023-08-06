
#ifndef _HTDB_H_
#define _HTDB_H_
#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>
#include <stdbool.h>
#include "dict.h"


// >> settings
// #define HTDB_TEST
typedef uint16_t xobjlen_t;
// << settings

typedef enum {
    XOBJ_TYPE_INT = 0,
    XOBJ_TYPE_BYTES = 1,
    // XOBJ_TYPE_FLOAT = 2,
    // XOBJ_TYPE_VARINT = 3,
    // XOBJ_TYPE_BOOL,
} xobj_type;

typedef struct {
    xobjlen_t len;
    uint8_t type;  // xobj_type
    char data[];
} xobj;

typedef struct {
    Dict *table;

} xdb;


xdb *xdbNew(char key_type, char val_type);
void xdbFree(xdb *db);
size_t xdbSize(xdb *db);
void xdbDump(xdb *db, FILE *stream);
void xdbLoad(xdb *db, FILE *stream);
int _xdbSetIntBytes(xdb *db, uint64_t key_, const char *value_, xobjlen_t value_len);
int _xdbSetIntInt(xdb *db, uint64_t key_, uint64_t value_);
int _xdbSetBytesBytes(xdb *db, const char *key_, xobjlen_t key_len, const char *value_, xobjlen_t value_len);
int _xdbGetIntBytes(xdb *db, uint64_t key_, char **value_, xobjlen_t *value_len);
int _xdbGetBytesBytes(xdb *db, const char *key_, xobjlen_t key_len, char **value_, xobjlen_t *value_len);
int _xdbGetIntInt(xdb *db, uint64_t key_, uint64_t *value);

xobj *xdbGetByInt(xdb *db, uint64_t key_);
xobj *xdbGetByBytes(xdb *db, const char *key_, xobjlen_t key_len);
bool xdbHasInt(xdb *db, uint64_t key_);
bool xdbHasBytes(xdb *db, const char *key_, xobjlen_t key_len);
bool xdbDelInt(xdb *db, uint64_t key_);
bool xdbDelBytes(xdb *db, const char *key_, xobjlen_t key_len);

#ifdef HTDB_TEST
void htdbTest(void);
#endif  // HTDB_TEST

#ifdef __cplusplus
}
#endif
#endif  // _HTDB_H_
