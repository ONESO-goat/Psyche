variables = {}

def run_line(line):
    parts = line.split()
    if not parts:
        return
    if parts[0] == 'print':
        if parts[1] in variables:
            print(parts[1])
            print(variables[parts[1]])
        else:
            print(" ".join(parts[1]))

    elif parts[0] == 'set':
        var_name = parts[1]
        value = int(parts[3])
        variables[var_name] = value
    
    elif parts[0] == 'add':
        var_name = parts[1]
        value = int(parts[2])
        variables[var_name] += value
    print(variables)

def run_program(code):
    lines = code.split("\n")
    print(f"LINES {lines}")
    for line in lines:
        print(f"CURRENT {line}")
        run_line(line)
program = """
set x = 5
add x 3
print x
""" 


def doc():
    info = """
    simple functions:
    
    print, exit, input, len, type, str(), int(), float(), bool(), list(), dict(), set(), tuple(), range()
    
    print = print a value to the console
    exit = exit the program
    input = get input from the user
    len = get the length of a string

    
    
    
    
    conditional statements:
    
    if, else, but, but if, change, and, or, not, >, <, >=, <=, ==, !=
    
    if = simple if statement
    else = fallback if if condition is not met
    but = like else but with a condition (elif)
    but if = like if but with a condition (elif)
    change = change the value of a variable
    and = logical AND
    or = logical OR
    not = logical NOT
    > = greater than
    < = less than
    >= = greater than or equal to
    <= = less than or equal to
    
    
    functions and classes:
    class, function, method, internalize, return, self
    
    class = define a class
    function = define a function
    method = define a method
    internalize = internalize the class
    return = return a value
    self = reference to the current instance of the class
    
    function vs method:
    function = a block of code that performs a specific task and can be called independently
    method = a function that is associated with an object and can access the object's data
    
    
    
    
    opterations:
    
    add, sub, mul, div, add*, sub*, mul*, div*, /, //, %, **, doesnt exist
    
    add = addition
    sub = subtraction
    mul = multiplication
    div = division
    add* = addition with assignment (example: x add* 2 => x = x + 2)
    sub* = subtraction with assignment (example: x sub* 2 => x = x - 2)
    mul* = multiplication with assignment (example: x mul* 2 => x = x * 2)
    div* = division with assignment (example: x div* 2 => x = x / 2)
    doesnt exist = check if a variable does not exist (example: x doesnt exist - checks if x is not defined in the current scope)

    / = division
    // = floor division
    % = modulo
    ** = exponentiation
    
    variables:
        
        const, int, float, str, bool, list, dict, set, tuple, is
        
        const = constant variable that cannot be changed
        int = integer variable
        float = floating point variable
        str = string variable
        bool = boolean variable
        list = list variable
        dict = dictionary variable
        set = set variable
        tuple = tuple variable
        is (identity operator: =) = identity operator (example: x is 10, y is x (y = 10), z is not y - z cannot equal to y)
    
    loops:
    
    for, stop, while (condition) is true, skip, loop, until
    
    for = for loop
    stop = stop the loop
    while (condition) is true = while loop (while x < 10 is true: do something)
    skip = skip the current iteration of the loop
    loop = infinite loop (loop: do something)
    until = loop until a condition is met (loop until x is 10: do something)
    
    
    unique syntax:
    
    note, tag, but if, but, change, is (identity operator), skip, loop until, is no, like (is like)
    
    note = a unique detail given to a variable (example: note x is a number between 1 and 10)
    tag = a label for a block of code (example: tag my_label: do something)
    but if = like if but with a condition (elif)
    like = like operator for comparisons (example: x is like y - checks if x and y are similar (x = 5, y = 9 => True because both are numbers))
    change = change the value of a variable (example: change x to 10)
    
    examples:
    
    int x is 5
    float y is 3.14
    str name is "John"
    bool is_true is True
    list items is [1, 2, 3]
    dict person is {"name": "John", "age": 30}
    set unique_items is {1, 2, 3}
    tuple coords is (10, 20)
    
    if x > 3:
        print "x is greater than 3"
    but if x == 3:
        print "x is equal to 3"
    but if x < 3:
        print "x is less than 3"
    else:
        print "x is not greater than 3"
        
    
    
    if x == z but if y > 2 and name is "John":
        loop until x is 10:
        
            x add* 1
            
            print "x is equal to z but y is greater than 2 and name is John"
    else:
        print "x is not equal to z or y is not greater than 2 or name is not John"
    
    list Pokemon is ["Pikachu", "Charmander", "Bulbasaur", "grimmsnarl"]
    for pokemon in Pokemon:
        print pokemon
    
    pokemon[3] note is "the best pokemon"
    while grimmsnarl.note is "the best pokemon":
        print "Grimmsnarl is the best pokemon"
        skip
    
    tag function function1(str name):
        print "Hello, " + name + "!"
        
        __tag__ is "This is a function that greets the user by name" => breaks the program without the tag syntax, but is a unique feature that allows you to give a function a tag that can be accessed later 
        
        (example:
        
    function1("Alice") => prints "Hello, Alice!"
    print function1.__tag__ => prints "This is a function that greets the user by name"
    
    class Pokemon:
        public str poke is "Pikachu"
        private note poke is "type is Electric"
        
        internalize Pokemon(
            str name,
            str type
        ):
        
        if name doesnt exist:
            print "Name is required"
            return
            
        if type doesnt exist:
            print "Type is required"
            return
            
        self.name = name
        self.type = type
        
        function show_info(self):
            print "Name: " + self.name
            print "Type: " + self.type
            print "Note: " + self.poke.note
            
        method evolve(self, new_form):
            print self.name + " is evolving into " + new_form + "!"
            self.name = new_form
           
            
            
    
    """
    return info.strip()