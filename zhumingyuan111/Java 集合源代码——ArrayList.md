---
title: Java 集合源代码——ArrayList
date: 2017-12-24 13:56:56
tags: CSDN迁移
---
  ArrayList 在开发中经常使用，今天有时间对其内部实现进行研究.

 
#### 先看看ArrayList的继承关系

 
```
public class ArrayList<E> extends AbstractList<E>
        implements List<E>, RandomAccess, Cloneable, java.io.Serializable
```
 可以看出ArrayList继承自AbstractList 并实现List接口。

 
```
/**
     * Default initial capacity.
     * 这里可以看出默认的数组大小是10
     */
    private static final int DEFAULT_CAPACITY = 10;

    /**
     * Shared empty array instance used for empty instances.
     * 这个是定义的空数组，这里是当初始化数组大小为0的时候使用
     */
    private static final Object[] EMPTY_ELEMENTDATA = {};

    /**
     * Shared empty array instance used for default sized empty instances. We
     * distinguish this from EMPTY_ELEMENTDATA to know how much to inflate when
     * 这里是初始化没有设定大小的时候使用。下面会给出源码。
     */

    private static final Object[] DEFAULTCAPACITY_EMPTY_ELEMENTDATA = {};
```
 
```
/**
     * The array buffer into which the elements of the ArrayList are stored.
     * The capacity of the ArrayList is the length of this array buffer. Any
     * empty ArrayList with elementData == DEFAULTCAPACITY_EMPTY_ELEMENTDATA
     * will be expanded to DEFAULT_CAPACITY when the first element is added.
     * 这个数组就是存储数据的结构
     */
    transient Object[] elementData; // non-private to simplify nested class access

    /**
     * The size of the ArrayList (the number of elements it contains).
     *
     * @serial
     * 记录数组大小
     */
    private int size;
```
 以下三个是ArrayList的构造函数

 
```
/**
     * Constructs an empty list with the specified initial capacity.
     *
     * @param  initialCapacity  the initial capacity of the list
     * @throws IllegalArgumentException if the specified initial capacity
     *         is negative
     * 可以看到当initialCapacity==0 的时候使用的是EMPTY_ELEMENTDATA
     */
    public ArrayList(int initialCapacity) {
        if (initialCapacity > 0) {
            this.elementData = new Object[initialCapacity];
        } else if (initialCapacity == 0) {
            this.elementData = EMPTY_ELEMENTDATA;
        } else {
            throw new IllegalArgumentException("Illegal Capacity: "+
                                               initialCapacity);
        }
    }

    /**
     * Constructs an empty list with an initial capacity of ten.
     * 这里用的是DEFAULTCAPACITY_EMPTY_ELEMENTDATA
     */
    public ArrayList() {
        this.elementData = DEFAULTCAPACITY_EMPTY_ELEMENTDATA;
    }

    /**
     * Constructs a list containing the elements of the specified
     * collection, in the order they are returned by the collection's
     * iterator.
     *
     * @param c the collection whose elements are to be placed into this list
     * @throws NullPointerException if the specified collection is null
     */
    public ArrayList(Collection<? extends E> c) {
        elementData = c.toArray();
        if ((size = elementData.length) != 0) {
            // c.toArray might (incorrectly) not return Object[] (see 6260652)
            if (elementData.getClass() != Object[].class)
                elementData = Arrays.copyOf(elementData, size, Object[].class);
        } else {
            // replace with empty array.
            this.elementData = EMPTY_ELEMENTDATA;
        }
    }
```
 
```
/**
     * Trims the capacity of this <tt>ArrayList</tt> instance to be the
     * list's current size.  An application can use this operation to minimize
     * the storage of an <tt>ArrayList</tt> instance.
     * 这个方法就是把缩小elementData大小，去掉多余的数组空间
     */
    public void trimToSize() {
        modCount++;
        if (size < elementData.length) {
            elementData = (size == 0)
              ? EMPTY_ELEMENTDATA
              : Arrays.copyOf(elementData, size);
        }
    }
```
 
```
/**
     * Increases the capacity of this <tt>ArrayList</tt> instance, if
     * necessary, to ensure that it can hold at least the number of elements
     * specified by the minimum capacity argument.
     *
     * @param   minCapacity   the desired minimum capacity
     * minExpand表示最小要扩展的数量
     * 这方法就是增加数组的大小，如果现在的数组是DEFAULTCAPACITY_EMPTY_ELEMENTDATA 那么minExpand就是（DEFAULT_CAPACITY）10
     * 否则，minExpand = 0
     */
    public void ensureCapacity(int minCapacity) {
        int minExpand = (elementData != DEFAULTCAPACITY_EMPTY_ELEMENTDATA)
            // any size if not default element table
            ? 0
            // larger than default for default empty table. It's already
            // supposed to be at default size.
            : DEFAULT_CAPACITY;

        if (minCapacity > minExpand) {
            ensureExplicitCapacity(minCapacity);
        }
    }
```
 
```
/**
*计算需要的空间
**/
   private static int calculateCapacity(Object[] elementData, int minCapacity) {
        if (elementData == DEFAULTCAPACITY_EMPTY_ELEMENTDATA) {
            return Math.max(DEFAULT_CAPACITY, minCapacity);
        }
        return minCapacity;
        }
```
 
```
//计算数组空间大小
private void ensureExplicitCapacity(int minCapacity) {
        modCount++;

        // overflow-conscious code
        if (minCapacity - elementData.length > 0)
            //这里是真正的增加空间
            grow(minCapacity);
    }
```
 
```
/**
     * Increases the capacity to ensure that it can hold at least the
     * number of elements specified by the minimum capacity argument.
     *
     * @param minCapacity the desired minimum capacity
     */
    private void grow(int minCapacity) {
        // overflow-conscious code
        //先把现在空间计算出来
        int oldCapacity = elementData.length;
        //这里增加的空间是以前空间的一半
        int newCapacity = oldCapacity + (oldCapacity >> 1);
        //如果新空间还是小于需要的大小，那么新的空间等于需要的空间
        if (newCapacity - minCapacity < 0)
            newCapacity = minCapacity;
            //需要大于最大空间，则进行大空间处理
        if (newCapacity - MAX_ARRAY_SIZE > 0)
            newCapacity = hugeCapacity(minCapacity);
        // minCapacity is usually close to size, so this is a win:
        //将对象拷贝到新数组
        elementData = Arrays.copyOf(elementData, newCapacity);
    }

    private static int hugeCapacity(int minCapacity) {
    //小于0，则直接报错啦
        if (minCapacity < 0) // overflow
            throw new OutOfMemoryError();
            //如果大于最大数组值，则赋值Int的最大值
        return (minCapacity > MAX_ARRAY_SIZE) ?
            Integer.MAX_VALUE :
            MAX_ARRAY_SIZE;
    }
```
 
```
//当我们用下标访问
@SuppressWarnings("unchecked")
    E elementData(int index) {
        return (E) elementData[index];
    }

    /**
     * Returns the element at the specified position in this list.
     *
     * @param  index index of the element to return
     * @return the element at the specified position in this list
     * @throws IndexOutOfBoundsException {@inheritDoc}
     * 这个就是get的实现
     */
    public E get(int index) {
    //检查index是否合法
        rangeCheck(index);

        return elementData(index);
    }
```
 
```
/**
     * Replaces the element at the specified position in this list with
     * the specified element.
     *
     * @param index index of the element to replace
     * @param element element to be stored at the specified position
     * @return the element previously at the specified position
     * @throws IndexOutOfBoundsException {@inheritDoc}
     * set函数将数组index的元素替换
     */
    public E set(int index, E element) {
        rangeCheck(index);

        E oldValue = elementData(index);
        elementData[index] = element;
        return oldValue;
    }
```
 
```
/**
     * Appends the specified element to the end of this list.
     *
     * @param e element to be appended to this list
     * @return <tt>true</tt> (as specified by {@link Collection#add})
     * add 函数在size的位置添加element
     */
    public boolean add(E e) {
    //这里可以看出每一次add的时候都需要确认是否需要增加空间
        ensureCapacityInternal(size + 1);  // Increments modCount!!
        elementData[size++] = e;
        return true;
    }
```
 
```
/**
     * Inserts the specified element at the specified position in this
     * list. Shifts the element currently at that position (if any) and
     * any subsequent elements to the right (adds one to their indices).
     *
     * @param index index at which the specified element is to be inserted
     * @param element element to be inserted
     * @throws IndexOutOfBoundsException {@inheritDoc}
     * 在index的位置添加element
     */
    public void add(int index, E element) {
    //检查index
        rangeCheckForAdd(index);
//增加空间
        ensureCapacityInternal(size + 1);  // Increments modCount!!
        //这里是把index之后的元素向后移动一个位置
        System.arraycopy(elementData, index, elementData, index + 1,
                         size - index);
        elementData[index] = element;
        size++;
    }
```
 
```
/**
     * Removes the element at the specified position in this list.
     * Shifts any subsequent elements to the left (subtracts one from their
     * indices).
     *
     * @param index the index of the element to be removed
     * @return the element that was removed from the list
     * @throws IndexOutOfBoundsException {@inheritDoc}
     * 删除index位置的元素
     */
    public E remove(int index) {
    //检查index
        rangeCheck(index);

        modCount++;
        E oldValue = elementData(index);

        int numMoved = size - index - 1;
        //拷贝index之后的元素，向前移动一位
        if (numMoved > 0)
            System.arraycopy(elementData, index+1, elementData, index,
                             numMoved);
        elementData[--size] = null; // clear to let GC do its work

        return oldValue;
    }
```
 
```
/*
     * Private remove method that skips bounds checking and does not
     * return the value removed.
     * 这个函数和remove非常类似，只不过没有检查数组越界情况以及没有返回值
     */
    private void fastRemove(int index) {
        modCount++;
        int numMoved = size - index - 1;
        if (numMoved > 0)
            System.arraycopy(elementData, index+1, elementData, index,
                             numMoved);
        elementData[--size] = null; // clear to let GC do its work
    }
```
 
```
/**
     * Removes the first occurrence of the specified element from this list,
     * if it is present.  If the list does not contain the element, it is
     * unchanged.  More formally, removes the element with the lowest index
     * <tt>i</tt> such that
     * <tt>(o==null&nbsp;?&nbsp;get(i)==null&nbsp;:&nbsp;o.equals(get(i)))</tt>
     * (if such an element exists).  Returns <tt>true</tt> if this list
     * contained the specified element (or equivalently, if this list
     * changed as a result of the call).
     *
     * @param o element to be removed from this list, if present
     * @return <tt>true</tt> if this list contained the specified element
     * 这里找到element之后调用fastRemove
     */
    public boolean remove(Object o) {
        if (o == null) {
            for (int index = 0; index < size; index++)
                if (elementData[index] == null) {
                    fastRemove(index);
                    return true;
                }
        } else {
            for (int index = 0; index < size; index++)
                if (o.equals(elementData[index])) {
                    fastRemove(index);
                    return true;
                }
        }
        return false;
    }
```
 
```
/**
     * Removes from this list all of its elements that are contained in the
     * specified collection.
     *
     * @param c collection containing elements to be removed from this list
     * @return {@code true} if this list changed as a result of the call
     * @throws ClassCastException if the class of an element of this list
     *         is incompatible with the specified collection
     * (<a href="Collection.html#optional-restrictions">optional</a>)
     * @throws NullPointerException if this list contains a null element and the
     *         specified collection does not permit null elements
     * (<a href="Collection.html#optional-restrictions">optional</a>),
     *         or if the specified collection is null
     * @see Collection#contains(Object)
     * remove all 将包含在Collection 中的元素全部删除
     */
    public boolean removeAll(Collection<?> c) {
        Objects.requireNonNull(c);
        return batchRemove(c, false);
    }
    //批量删除方法
private boolean batchRemove(Collection<?> c, boolean complement) {
        final Object[] elementData = this.elementData;
        int r = 0, w = 0;
        boolean modified = false;
        try {
            for (; r < size; r++)
            //当complement为false的时候，经过这次循环前w的元素是要保留的。
                if (c.contains(elementData[r]) == complement)
                    elementData[w++] = elementData[r];
        } finally {
            // Preserve behavioral compatibility with AbstractCollection,
            // even if c.contains() throws.
            if (r != size) {
            //这种情况是因为差c.contains()发生错误，则进行元素拷贝
                System.arraycopy(elementData, r,
                                 elementData, w,
                                 size - r);
                w += size - r;
            }
            if (w != size) {
            //将w后面的元素设置为null
                // clear to let GC do its work
                for (int i = w; i < size; i++)
                    elementData[i] = null;
                modCount += size - w;
                size = w;
                modified = true;
            }
        }
        return modified;
    }
```
 以下是ArrayList 的Iterator实现

 
```
/**
     * Returns an iterator over the elements in this list in proper sequence.
     *
     * <p>The returned iterator is <a href="#fail-fast"><i>fail-fast</i></a>.
     *
     * @return an iterator over the elements in this list in proper sequence
     */
    public Iterator<E> iterator() {
        return new Itr();
    }
/**
     * An optimized version of AbstractList.Itr
     */
    private class Itr implements Iterator<E> {
       //指向下一次返回element的位置
        int cursor;       // index of next element to return 
        //指向上一次（前一次）返回element的位置， -1则是没有的情况下
        int lastRet = -1; // index of last element returned; -1 if no such
        //我们都知道在迭代的过程中是不允许增加或者删除List中的元素的，这里expectedModCount记录修改次数，后面在每一次迭代中都会检查这个值是否发生变化
        int expectedModCount = modCount;
//数组的下标是0 --> size-1,如果cursor==size则不会有下一个元素
        public boolean hasNext() {
            return cursor != size;
        }

        @SuppressWarnings("unchecked")
        public E next() {
        //检查expectedModCount是否发生变化
            checkForComodification();
            int i = cursor;
            if (i >= size)//这种情况说明已经没有元素啦
                throw new NoSuchElementException();
            Object[] elementData = ArrayList.this.elementData;
            if (i >= elementData.length)//可能有其他线程修改数组长度，会出现这种情况
                throw new ConcurrentModificationException();
            cursor = i + 1;//cursor+1
            //给lastRet赋值，并返回元素
            return (E) elementData[lastRet = i];
        }

        public void remove() {
            if (lastRet < 0)//记得在初始化的时候lastRet=-1
            所以调用next()之后才能调用remove方法
                throw new IllegalStateException();
            checkForComodification();

            try {
            //调用ArrayList中的remove方法
                ArrayList.this.remove(lastRet);
                cursor = lastRet;//这里cursor相当于减1
                lastRet = -1;//lastRet并没有减1而是直接赋值-1，所以如果我们连续调用两次remove()则会出错
                expectedModCount = modCount;//expectedModCount值更新，因为前面的ArrayList.this.remove(lastRet)改变了modCount的值
            } catch (IndexOutOfBoundsException ex) {
                throw new ConcurrentModificationException();
            }
        }
```
 
```
/**
     * An optimized version of AbstractList.ListItr
     * ListItr 则是Itr的加强版，增加了双向的迭代方法
     */
    private class ListItr extends Itr implements ListIterator<E> {
        ListItr(int index) {
            super();
            cursor = index;
        }
//是否有前一个
        public boolean hasPrevious() {
            return cursor != 0;
        }
//下一个index
        public int nextIndex() {
            return cursor;
        }
//previous index
        public int previousIndex() {
            return cursor - 1;
        }
//返回previous元素
        @SuppressWarnings("unchecked")
        public E previous() {
        ////检查expectedModCount是否发生变化
            checkForComodification();
            int i = cursor - 1;//i指向当前元素的前一个位置
            if (i < 0)//i 不合法
                throw new NoSuchElementException();
            Object[] elementData = ArrayList.this.elementData;
            if (i >= elementData.length)//i超过了数组长度
                throw new ConcurrentModificationException();
            cursor = i;//相当于cursor向前移动一个位置
            return (E) elementData[lastRet = i];
        }

//用e 替换lastRet位置元素
        public void set(E e) {
            if (lastRet < 0)
                throw new IllegalStateException();
            checkForComodification();

            try {
                ArrayList.this.set(lastRet, e);
            } catch (IndexOutOfBoundsException ex) {
                throw new ConcurrentModificationException();
            }
        }
//在cursor位置添加元素
        public void add(E e) {
            checkForComodification();

            try {
                int i = cursor;
                ArrayList.this.add(i, e);
                cursor = i + 1;
                lastRet = -1;
                expectedModCount = modCount;
            } catch (IndexOutOfBoundsException ex) {
                throw new ConcurrentModificationException();
            }
        }
    }
```
   
  