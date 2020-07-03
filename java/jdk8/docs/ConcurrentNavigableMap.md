import java.util.concurrent.ConcurrentNavigableMap;
import java.util.concurrent.ConcurrentSkipListMap;

public class TestThread {

   public static void main(final String[] arguments){
      ConcurrentNavigableMap<String,String> map = new ConcurrentSkipListMap<String, String>();
      map.put("1", "One");
      map.put("2", "Two");
      map.put("3", "Three");
      map.put("5", "Five");
      map.put("6", "Six");
      System.out.println("Initial ConcurrentHashMap: "+map);
      System.out.println("HeadMap(\"2\") of ConcurrentHashMap: "+map.headMap("2"));
      System.out.println("TailMap(\"2\") of ConcurrentHashMap: "+map.tailMap("2"));
      System.out.println("SubMap(\"2\", \"4\") of ConcurrentHashMap: "+map.subMap("2","4"));
   }  
}


Initial ConcurrentHashMap: {1=One, 2=Two, 3=Three, 5=Five, 6=Six}
HeadMap("2") of ConcurrentHashMap: {1=One}
TailMap("2") of ConcurrentHashMap: {2=Two, 3=Three, 5=Five, 6=Six}
SubMap("2", "4") of ConcurrentHashMap: {2=Two, 3=Three}




// 构造一个新的空映射，该映射按照键的自然顺序进行排序。
ConcurrentSkipListMap()
// 构造一个新的空映射，该映射按照指定的比较器进行排序。
ConcurrentSkipListMap(Comparator<? super K> comparator)
// 构造一个新映射，该映射所包含的映射关系与给定映射包含的映射关系相同，并按照键的自然顺序进行排序。
ConcurrentSkipListMap(Map<? extends K,? extends V> m)
// 构造一个新映射，该映射所包含的映射关系与指定的有序映射包含的映射关系相同，使用的顺序也相同。
ConcurrentSkipListMap(SortedMap<K,? extends V> m)
// 返回与大于等于给定键的最小键关联的键-值映射关系；如果不存在这样的条目，则返回 null。
Map.Entry<K,V> ceilingEntry(K key)
// 返回大于等于给定键的最小键；如果不存在这样的键，则返回 null。
K ceilingKey(K key)
// 从此映射中移除所有映射关系。
void clear()
// 返回此 ConcurrentSkipListMap 实例的浅表副本。
ConcurrentSkipListMap<K,V> clone()
// 返回对此映射中的键进行排序的比较器；如果此映射使用键的自然顺序，则返回 null。
Comparator<? super K> comparator()
// 如果此映射包含指定键的映射关系，则返回 true。
boolean containsKey(Object key)
// 如果此映射为指定值映射一个或多个键，则返回 true。
boolean containsValue(Object value)
// 返回此映射中所包含键的逆序 NavigableSet 视图。
NavigableSet<K> descendingKeySet()
// 返回此映射中所包含映射关系的逆序视图。
ConcurrentNavigableMap<K,V> descendingMap()
// 返回此映射中所包含的映射关系的 Set 视图。
Set<Map.Entry<K,V>> entrySet()
// 比较指定对象与此映射的相等性。
boolean equals(Object o)
// 返回与此映射中的最小键关联的键-值映射关系；如果该映射为空，则返回 null。
Map.Entry<K,V> firstEntry()
// 返回此映射中当前第一个（最低）键。
K firstKey()
// 返回与小于等于给定键的最大键关联的键-值映射关系；如果不存在这样的键，则返回 null。
Map.Entry<K,V> floorEntry(K key)
// 返回小于等于给定键的最大键；如果不存在这样的键，则返回 null。
K floorKey(K key)
// 返回指定键所映射到的值；如果此映射不包含该键的映射关系，则返回 null。
V get(Object key)
// 返回此映射的部分视图，其键值严格小于 toKey。
ConcurrentNavigableMap<K,V> headMap(K toKey)
// 返回此映射的部分视图，其键小于（或等于，如果 inclusive 为 true）toKey。
ConcurrentNavigableMap<K,V> headMap(K toKey, boolean inclusive)
// 返回与严格大于给定键的最小键关联的键-值映射关系；如果不存在这样的键，则返回 null。
Map.Entry<K,V> higherEntry(K key)
// 返回严格大于给定键的最小键；如果不存在这样的键，则返回 null。
K higherKey(K key)
// 如果此映射未包含键-值映射关系，则返回 true。
boolean isEmpty()
// 返回此映射中所包含键的 NavigableSet 视图。
NavigableSet<K> keySet()
// 返回与此映射中的最大键关联的键-值映射关系；如果该映射为空，则返回 null。
Map.Entry<K,V> lastEntry()
// 返回映射中当前最后一个（最高）键。
K lastKey()
// 返回与严格小于给定键的最大键关联的键-值映射关系；如果不存在这样的键，则返回 null。
Map.Entry<K,V> lowerEntry(K key)
// 返回严格小于给定键的最大键；如果不存在这样的键，则返回 null。
K lowerKey(K key)
// 返回此映射中所包含键的 NavigableSet 视图。
NavigableSet<K> navigableKeySet()
// 移除并返回与此映射中的最小键关联的键-值映射关系；如果该映射为空，则返回 null。
Map.Entry<K,V> pollFirstEntry()
// 移除并返回与此映射中的最大键关联的键-值映射关系；如果该映射为空，则返回 null。
Map.Entry<K,V> pollLastEntry()
// 将指定值与此映射中的指定键关联。
V put(K key, V value)
// 如果指定键已经不再与某个值相关联，则将它与给定值关联。
V putIfAbsent(K key, V value)
// 从此映射中移除指定键的映射关系（如果存在）。
V remove(Object key)
// 只有目前将键的条目映射到给定值时，才移除该键的条目。
boolean remove(Object key, Object value)
// 只有目前将键的条目映射到某一值时，才替换该键的条目。
V replace(K key, V value)
// 只有目前将键的条目映射到给定值时，才替换该键的条目。
boolean replace(K key, V oldValue, V newValue)
// 返回此映射中的键-值映射关系数。
int size()
// 返回此映射的部分视图，其键的范围从 fromKey 到 toKey。
ConcurrentNavigableMap<K,V> subMap(K fromKey, boolean fromInclusive, K toKey, boolean toInclusive)
// 返回此映射的部分视图，其键值的范围从 fromKey（包括）到 toKey（不包括）。
ConcurrentNavigableMap<K,V> subMap(K fromKey, K toKey)
// 返回此映射的部分视图，其键大于等于 fromKey。
ConcurrentNavigableMap<K,V> tailMap(K fromKey)
// 返回此映射的部分视图，其键大于（或等于，如果 inclusive 为 true）fromKey。
ConcurrentNavigableMap<K,V> tailMap(K fromKey, boolean inclusive)
// 返回此映射中所包含值的 Collection 视图。
Collection<V> values()




ConcurrentSkipListMap
https://blog.csdn.net/coslay/article/details/44819823




CountDownLatch也是基于AQS，它是AQS的共享功能的一个实现。
http://ifeve.com/countdownlatch%E6%BA%90%E7%A0%81%E8%A7%A3%E6%9E%90/

