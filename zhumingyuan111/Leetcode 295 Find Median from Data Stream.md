---
title: Leetcode 295 Find Median from Data Stream
date: 2019-03-02 13:24:19
tags: CSDN迁移
---
  ### []()题目链接：[https://leetcode.com/problems/find-median-from-data-stream/](https://leetcode.com/problems/find-median-from-data-stream/)

 
### []()解题思路

 既然是是找到中位数，我们就使用两个堆，一个是大顶堆，一个小顶堆，保证两个堆满足以下条件：

  
  2. 大顶堆的第一个元素需要小于小顶堆的第一个元素； 
  4. 大顶堆的元素数量不能小于小顶堆且最多只能多一个元素；  
      满足以上条件，需要找中位数的时候，判断大顶堆是否比小顶堆元素多，如果多，直接返回大顶堆的第一个元素，否则将大，小顶堆的元素相加再除2，下面给出代码，随便使用golang重写以下堆排序。  
```
import "fmt"

type Heap struct {
	array []int32
	f func(x int32,y int32) bool
}

func NewHeapInstance(f func(x int32,y int32) bool) *Heap{
	return &Heap{array:make([]int32,0,10),f:f}
}

func (h *Heap) Sort() {
	i := len(h.array)
	for ; i > 1; i-- {
		h.swap(i - 1,1)
		h.sink(1, i - 2)
	}
}

func (h *Heap) Create(array[]int32) {
	h.array = array
	i := len(h.array) / 2
	for ;i != 0; i-- {
		h.sink(i,len(array)-1)
	}
}

func (h *Heap) sink(index int,l int) {
	leftI := index * 2
	if leftI > l {
		return
	}
	var tmpI = 0
	rightI := index * 2 + 1

	if rightI > l {
		tmpI = leftI
	} else if h.f(h.array[leftI],h.array[rightI]) {
		tmpI = leftI
	} else {
		tmpI = rightI
	}
	if h.f(h.array[index],h.array[tmpI]) {
		return
	} else {
		h.swap(index,tmpI)
		h.sink(tmpI,l)
	}
}

func (h *Heap) sift(index int) {
	parentI := index / 2
	if parentI == 0 {
		return
	}
	if h.f(h.array[parentI],h.array[index]) {
		return
	} else {
		h.swap(parentI,index)
		h.sift(parentI)
	}
}

func (h *Heap) Put(x int32) {
	if len(h.array) == 0 {
		h.array = append(h.array,0)
	}
	h.array = append(h.array,x)
	l := len(h.array)
	h.sift(l-1)
}

func (h *Heap) Get() int32 {
	if len(h.array) > 1 {
		return h.array[1]
	} else {
		panic("heap is empty !")
	}
}

func (h *Heap) Pop() int32 {
	if len(h.array) <= 1 {
		panic("heap is empty !")
	} else {
		res := h.array[len(h.array) -1]
		h.swap(1, len(h.array) - 1)
		h.array = h.array[:len(h.array) - 1]
		h.sink(1, len(h.array)-1)
		return res
	}
}

func (h *Heap) Print() {
	for i,v := range h.array {
		fmt.Printf("index: %d, val: %d\n", i ,v)
	}
}

func (h *Heap) swap(i int, j int) {
	tmp := h.array[i]
	h.array[i] = h.array[j]
	h.array[j] = tmp
}

type MedianFinder struct {
	minHeap *Heap
	maxHeap *Heap
}


/** initialize your data structure here. */
func Constructor() MedianFinder {
	minHeap := NewHeapInstance(func(x int32, y int32) bool {
		if x < y {
			return true
		} else {
			return false
		}
	})
	maxHeap := NewHeapInstance(func(x int32, y int32) bool {
		if x < y {
			return false
		} else {
			return true
		}
	})
	return MedianFinder{minHeap:minHeap,maxHeap:maxHeap}
}


func (this *MedianFinder) AddNum(num int)  {
	if len(this.maxHeap.array) == len(this.minHeap.array) {
		this.maxHeap.Put(int32(num))
	} else {
		this.minHeap.Put(int32(num))
	}
	this.balance()
}


func (this *MedianFinder) FindMedian() float64 {
	if len(this.maxHeap.array) > len(this.minHeap.array) {
		return float64(this.maxHeap.Get())
	} else {
		return (float64(this.maxHeap.Get()) + float64(this.minHeap.Get())) / 2
	}
}

func (this *MedianFinder) balance() {
	if len(this.minHeap.array) == 0 {
		return
	}
	minT := this.minHeap.Get()
	maxT := this.maxHeap.Get()
	if maxT > minT {
		this.maxHeap.Pop()
		this.minHeap.Pop()
		this.minHeap.Put(int32(maxT))
		this.maxHeap.Put(int32(minT))
	}
}



```
   
  