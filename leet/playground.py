
# O <-> A <-> B <-> C <-> D <-> O is what it looks like

# I have a node class which has a key, value,
# WHen I create an LRUCahce i'd want it too look like dummy <-> dummy
# get, put,
# So this is least recently used cache. whenever I get something, it needs to be updated to the front of the list
# also, when I remove something I need to reconnect the nodes accordingly
# that was easy. lol *sweat,

# Wow. LRU Cache actually hard to understand and implement lol. Literally took me like 3-4 hrs to fully understand and do it haha
# MY LRU Cache Implementation: 1st time took about 4 hours with a lot of llm conversation.

class Node:
    def __init__(self, key, value):
        self.key = key      # we store the key too — you'll see why in eviction
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # key -> Node, gives us O(1) lookup

        # Dummy head/tail sentinel nodes — this avoids messy None-checks
        # when inserting/removing at the boundaries
        self.head = Node(0, 0)  # most-recently-used side
        self.tail = Node(0, 0)  # least-recently-used side
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        # Unlink node from wherever it currently sits — O(1)
        node.prev.next = node.next
        node.next.prev = node.prev

    def _insert_at_front(self, node):
        # Always insert right after head = most recently used position
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)
        self._insert_at_front(node)  # accessing it = it's now most recently used
        return node.value

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            # Update existing node's value and bump its recency
            node = self.cache[key]
            node.value = value
            self._remove(node)
            self._insert_at_front(node)
            return

        if len(self.cache) >= self.capacity:
            # Evict least recently used = node just before tail sentinel
            lru_node = self.tail.prev
            self._remove(lru_node)
            del self.cache[lru_node.key]  # <-- this is why Node stores `key`

        new_node = Node(key, value)
        self.cache[key] = new_node
        self._insert_at_front(new_node)


#######################################################################################################################################################


# LRU Cache 2nd time est 25 mins for completion.
# Basically for this problem I nead some sort of a map since I need to do this in O(1). Also, since I need to keep track of what's least recently used I need to use a double linked list.
# Lets start making our nodes, and then the actual data structure.

class Node:
    def _init_(self, key, value):
        # key value makes sense
        self.key = key
        self.value = value
        # makes sense to also set the tail and prev here...
        self.tail = None
        self.head = None

class LRUCache:
    def _init_(self, capacity):
        self.capacity = self.capacity
        lru_cache = {}
        # important for the tracking of our head and tail or else we have to do some funky stuff 
        self.head = Node(0,0)
        self.tail = Node(0,0)
        # forgot about their pointers
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        self.prev.next = node.next
        self.next.prev = node.prev

    def _put_at_front(self, node):
        # takes care of the node pointers
        node.next = self.head.next
        node.prev = self.head
        # now the head pointer
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        node = self.cache[key]
        self._remove(node)
        self._put_at_front(node)
        return node.value

    def put(self, key, value):
        if (key in self.lru_cache):
            same_key_node = self.cache[key]
            self._remove(same_key_node)
            self._put_at_front(same_key_node)
            return

        if (self.cache >= self.capacity):
            #trim tail
            lru_node = self.tail.prev
            self._remove(lru_node)
            del self.cache[lru_node.key]

        new_node = Node(key,value)
        self._put_at_front(new_node)

# wow. That took much much quicker this time. Like 25 mins top.
###################################################################################################################################################################################################

# Daily Temperature
temperatures = [73, 74, 75, 71, 69, 72, 76, 73]
# answer        = [ 1,  1,  4,  2,  1,  1,  0,  0]
answer = []
for enumerate t,i in temperatures
    current_temp = t
    for enumerate() k, j in temperatures
    next_value = temperatures[j + 1]
    if current_temp < next_value:
        push(j+1) onto answer array

# this works I guess, but there is a better wway to do this.

