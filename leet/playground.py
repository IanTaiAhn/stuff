
# O <-> A <-> B <-> C <-> D <-> O is what it looks like

# I have a node class which has a key, value,
# WHen I create an LRUCahce i'd want it too look like dummy <-> dummy
# get, put,
# So this is least recently used cache. whenever I get something, it needs to be updated to the front of the list
# also, when I remove something I need to reconnect the nodes accordingly
# that was easy. lol *sweat,

# Wow. LRU Cache actually hard to understand and implement lol. Literally took me like 3-4 hrs to fully understand and do it haha
# MY LRU Cache Implementation:

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int) # controlling capacity to be an int.
        self.capacity = capacity
        self.cache = {}

        self.head = Node(0,0)
        self.tail = Node(0,0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    # I'll call this within my get...
    def _insert_at_front(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def _get(self, key):
        if key not in self.cache:
            return-1
        node = self.cache(key)
        self._remove(node)
        self._insert_at_front(node)
        return node.value

    def _put(self, key, value):
        if key in self.cache:
            node = self.cache(key)
            node.value = value
            self._remove(node)
            self._insert_at_front(node)
            return
        if len(self.cache) >= self.capacity:
            lru_node = self.tail.prev
            self._remove(lru_node)
            del self.cache[lru_node.key]
        new_node = Node(key, value)
        self._insert_at_front(new_node)


#######################################################################################################################################################


