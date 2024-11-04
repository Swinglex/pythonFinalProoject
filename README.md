# pythonFinalProoject
big cool
House Remodeling Supply Tracker
Objective:

You will build a Python web application using Flask and SQLAlchemy to track the supplies and costs needed for remodeling various rooms in a house. The application will allow users to enter detailed information about each room, including the type of remodeling (tiling, flooring, painting, etc.) and the materials required. The app will calculate total remodeling costs, display detailed breakdowns, and visualize data using Seaborn bar graphs.
This project will require:

•	SQLAlchemy models with foreign key relationships.
•	Instantiable classes and complex data handling using dictionaries, tuples, and lists.
•	Unit tests using PyTest to validate application functionality.
•	A web interface to add, edit, and display room and supply data.
•	A Seaborn bar graph to visually represent the data.


Project Requirements:

1. SQLAlchemy Models:
You will create two main models: Room and Supply. Each room will have a list of associated supplies and costs.

Room Model:
•	id: Primary key (integer).
•	name: The name of the room (string).
•	surface_area: Total surface area of the room in square feet (float).
•	flooring_type: Type of flooring (e.g., "Hardwood", "Tile") (string).
•	flooring_cost_per_sqft: Cost of the flooring per square foot (float).
•	New Fields:
o	is_tiling_needed: Boolean indicating whether tiling is needed (boolean).
o	tile_type: Type of tile (e.g., "Ceramic", "Porcelain") (string).
o	tile_cost_per_sqft: Cost of tiling per square foot (float).
o	tiling_area: Area of the room that requires tiling (float).
o	total_tile_cost: Calculated field for the total cost of tiling (tiling_area * tile_cost_per_sqft).
o	total_flooring_cost: Total cost for the flooring, calculated as surface_area * flooring_cost_per_sqft.
o	total_remodel_cost: Calculated field for the total remodeling cost (sum of flooring, tiling, and supply costs).

Supply Model:
•	id: Primary key (integer).
•	room_id: Foreign key linking to the Room model.
•	name: Name of the supply (string).
•	quantity: Quantity of the supply needed (integer).
•	cost_per_item: Cost of each supply item (float).
•	total_supply_cost: Calculated field for the total cost of the supply (quantity * cost_per_item).

Foreign Key Relationship:
•	room_id in Supply will be a foreign key that references id in the Room model.

2. Web Application Pages:

Home Page:
•	Lists all the rooms that are being remodeled.
•	Displays total remodeling costs for each room.

Add Room Page:
•	Form to add a new room, capturing:
o	Room name.
o	Surface area in square feet.
o	Flooring type and cost per square foot.
o	Checkbox for tiling requirement (if applicable).
o	Tile type, cost per square foot, and tiling area (if applicable).
o	Button to submit room details.

Edit Room Page:
•	Form pre-filled with existing room data to allow updating information.

Room Details Page:
•	Displays the details for a specific room, including:
o	Flooring type and cost.
o	Tiling information (if tiling is required).
o	Total costs for flooring, tiling, and supplies.
o	A list of all associated supplies and their costs.
o	A total remodeling cost for the room, which is:
	total_remodel_cost = total_flooring_cost + total_tile_cost + sum(supply.total_supply_cost for supply in room.supplies)

Add Supply Page:
•	Form to add supplies to a specific room:
o	Supply name.
o	Quantity.
o	Cost per item.
o	Button to submit supply details.


Supply Details Page:
•	Displays details of a specific supply, including total cost.

3. Advanced Calculations:

Total Room Remodeling Cost:
o	total_remodel_cost = total_flooring_cost + total_tile_cost + sum(supply.total_supply_cost for supply in room.supplies)
This calculation includes:
•	Flooring cost (surface_area * flooring_cost_per_sqft).
•	Tiling cost (if applicable: tiling_area * tile_cost_per_sqft).
•	Supply costs (quantity * cost_per_item for each supply).

Tile Needed Calculation:
•	total_tile_cost = tiling_area * tile_cost_per_sqft

4. Seaborn Bar Graph Visualization:

You will create a Seaborn bar graph on a separate page that compares the total tiling costs or total remodeling costs across all rooms.
•	X-axis: Room names.
•	Y-axis: Total tiling cost (or total remodeling cost).
•	This graph will allow users to quickly visualize and compare costs between rooms.

5. Unit Testing with PyTest:

You will create unit tests to ensure the correctness of your calculations and functionality.
•	You are developing your code. You need to be able to estimate what 80% coverage is based on what you build. It is your job as a developer to develop that deeper level of understanding.



