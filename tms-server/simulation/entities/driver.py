import itertools
import random
import simpy.rt
import requests
import concurrent.futures

"""
A warehouse has a limited number of loading docks. Drivers arrive randomly at the warehouse, request a loading dock, 
and start loading or unloading their truck. The warehouse manages multiple products, each with its own inventory levels 
and reorder thresholds.

A warehouse control process (WMS) observes inventory levels and calls for a driver when inventory is needed. If multiple 
products from the same warehouse require replenishment, the control process will try to consolidate these orders to use 
a single driver whenever possible.

Each product in the inventory has a certain quantity and a reorder level. When the inventory drops below the reorder 
level, the WMS generates a reorder request. This request includes the order ID, timestamp, warehouse ID, and the list 
of products needing restock along with their quantities and priority levels. The WMS sends this reorder request to the 
Transportation Management System (TMS).

The TMS receives the reorder request and processes it by scheduling a driver and allocating a loading dock. The TMS can 
plan multi-stop routes for the driver if products need to be picked up from multiple locations. The Warehouse Manager 
in the TMS is notified of the new reorder request, can review the request details, and take necessary actions to fulfill 
the order.

If the products in a single reorder request need to be picked up from different locations, the TMS can:

Plan a multi-stop route for a single driver.
Use consolidation centers to combine products from various suppliers.
Coordinate partial shipments to ensure timely delivery of critical items.
The inventory decreases over time as products are sold, and the WMS continuously monitors and updates the inventory levels 
in real-time. The Warehouse Manager in the TMS can monitor the status of reorder requests, including driver assignments and 
shipment progress, ensuring timely replenishment of inventory.

"""

DOCKS = 6
LOADING_TIME = random.randint(1, 5)
UNLOADING_TIME = random.randint(1, 15)
TRAVEL_TIME = random.randint(6, 20)
REORDER_LEVEL = 50
MAX_INVENTORY = 100
INVENTORY_DECRESE_RATE = 10
PRODUCT_TYPES = 10
SIM_TIME = 100
COUNT = 0
DRIVER_WAIT_TIME = dict()


class Warehouse:
    def __init__(self, env):
        self.inventories = dict()
        self.inventory_requests = dict()

        for i in range(PRODUCT_TYPES):
            inventory_quantity = random.randint(30, MAX_INVENTORY)
            inventory = simpy.Container(
                env, init=inventory_quantity, capacity=MAX_INVENTORY
            )
            self.inventory_requests[i] = False
            self.inventories[i] = inventory

        self.docks = simpy.Resource(env, capacity=DOCKS)
        self.monitor_inventory = env.process(self.monitor_inventory(env))

    def monitor_inventory(self, env):
        """
        Periodically check the inventory levels and call for a driver when the inventory
        drops below the reorder level.
        """
        while True:
            for product, inventory in self.inventories.items():
                if (
                    inventory.level < REORDER_LEVEL
                    and not self.inventory_requests[product]
                ):
                    self.inventory_requests[product] = True
                    print(
                        "ACTION: Calling for driver for product {} at time {}".format(
                            product, env.now
                        )
                    )
                    env.process(self.place_request(env))
                    global COUNT
                    env.process(driver(env, COUNT, self, product))
                    COUNT += 1

            yield env.timeout(10)  # Check inventory every 10 time units

    def place_request(self, env):
        print(
            "ACTION: Requesting more product from supplier at time {}".format(env.now)
        )
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(fetch_data)
        yield env.timeout(1)


def fetch_data():
    res = requests.get("http://localhost:5000/api/admin/test")
    print("Received text")


def driver(env, name, warehouse, product):
    """
    Driver arrives at warehouse or supplier after a certain travel time, requests a loading dock if
    at the warehouse, and loads/unloads the product.
    """
    yield env.timeout(TRAVEL_TIME)
    amount = (
        warehouse.inventories[product].capacity - warehouse.inventories[product].level
    )
    yield env.timeout(LOADING_TIME)
    print(
        "CHECK: Driver {} loaded {} units of product {} at time {}".format(
            name, amount, product, env.now
        )
    )
    yield env.timeout(TRAVEL_TIME)
    print("CHECK: Driver {} arriving at warehouse at time {}".format(name, env.now))
    print("ACTION: Driver {} requesting loading dock at time {}".format(name, env.now))
    with warehouse.docks.request() as request:
        yield request
        print("CHECK: Driver {} loading dock acquired at time {}".format(name, env.now))
        yield env.timeout(UNLOADING_TIME)
        print(
            "ACTION: Driver {} unloaded product {} at time {}".format(
                name, product, env.now
            )
        )
        yield warehouse.inventories[product].put(amount)
        warehouse.inventory_requests[product] = False
        print("CHECK: Inventory levels at time {} are: ".format(env.now), end="")
        print([inventory.level for inventory in warehouse.inventories.values()])


def sell_product(warehouse, product, amount):
    """
    Sell product to customer and decrease inventory levels.
    """
    yield warehouse.inventories[product].get(amount)


def costumer_generator(env, warehouse):
    """
    Decrease the inventory levels over time as product is sold.
    """
    for i in itertools.count():
        yield env.timeout(random.randint(1, 10))
        bought = random.randint(1, 5)
        product = random.randint(0, PRODUCT_TYPES - 1)
        env.process(sell_product(warehouse, product, bought))


"""
The simulation flow is as follows:
1. Create the simulation environment
2. Create the warehouse control process
    The warehouse control process periodically checks the inventory levels and calls for a driver
    when the inventory drops below the reorder level.
3. Create the driver process
    The driver process arrives at the warehouse or supplier after a certain travel time, requests a loading dock
    if at the warehouse, and loads/unloads the product.
4. Create the inventory decrease process
    The inventory decrease process decreases the inventory levels over time as product is sold.
5. Start the simulation
    The simulation runs until the simulation time is reached.

"""


def main():

    # Setup and start the simulation
    print("Warehouse Simulation")
    random.seed(42)

    # Create the simulation environment
    env = simpy.rt.RealtimeEnvironment(factor=0.1, strict=False)
    warehouse = Warehouse(env)
    costumer_gen = env.process(costumer_generator(env, warehouse))

    env.run(until=SIM_TIME)

    print("Driver wait times: ", DRIVER_WAIT_TIME)


if __name__ == "__main__":
    main()
