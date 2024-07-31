# tbox

https://github.com/tboox/tbox/

c语言写的

https://docs.tboox.org/

## 编译


## api
### 容器

```c
    // init vector
    tb_vector_ref_t vector = tb_vector_init(0, tb_element_str(tb_true));
    if (vector)
    {
        // insert item
        tb_vector_insert_tail(vector, "hello");
        tb_vector_insert_tail(vector, "tbox");

        // dump all items
        tb_for_all (tb_char_t const*, cstr, vector)
        {
            // trace
            tb_trace_i("%s", cstr);
        }

        // exit vector
        tb_vector_exit(vector);
    }
```
## 自己的代码

https://github.com/sandisks/ctestttbox

