"""
Fallback questions database for when API is unavailable
Provides MCQ questions for common programming skills
"""

FALLBACK_MCQ_QUESTIONS = {
    "Python": {
        "beginner": [
            {
                "question": "What is the output of print(2 ** 3)?",
                "options": {
                    "A": "6",
                    "B": "8",
                    "C": "5",
                    "D": "23"
                },
                "correct_answer": "B",
                "explanation": "** is the exponentiation operator. 2 ** 3 = 2 * 2 * 2 = 8"
            },
            {
                "question": "Which function returns the length of a string?",
                "options": {
                    "A": "length()",
                    "B": "size()",
                    "C": "len()",
                    "D": "count()"
                },
                "correct_answer": "C",
                "explanation": "The len() function returns the number of characters in a string"
            },
            {
                "question": "What is the correct syntax to create a list in Python?",
                "options": {
                    "A": "list = (1, 2, 3)",
                    "B": "list = [1, 2, 3]",
                    "C": "list = {1, 2, 3}",
                    "D": "list = <1, 2, 3>"
                },
                "correct_answer": "B",
                "explanation": "Square brackets [] are used to create lists. Parentheses create tuples, curly braces create sets."
            },
            {
                "question": "What does the append() method do?",
                "options": {
                    "A": "Removes an element from a list",
                    "B": "Adds an element to the end of a list",
                    "C": "Sorts the list",
                    "D": "Returns the last element"
                },
                "correct_answer": "B",
                "explanation": "append() adds a single item to the end of a list"
            },
            {
                "question": "How do you create a dictionary with key-value pairs?",
                "options": {
                    "A": "dict = [key: value]",
                    "B": "dict = {key: value}",
                    "C": "dict = (key: value)",
                    "D": "dict = <key: value>"
                },
                "correct_answer": "B",
                "explanation": "Dictionaries are created using curly braces with key: value pairs"
            }
        ],
        "intermediate": [
            {
                "question": "What is the difference between == and 'is' in Python?",
                "options": {
                    "A": "No difference, they are identical",
                    "B": "== compares values, 'is' compares object identity",
                    "C": "'is' is only for integers",
                    "D": "== is deprecated in Python 3"
                },
                "correct_answer": "B",
                "explanation": "== checks if values are equal, while 'is' checks if two references point to the same object"
            },
            {
                "question": "What does *args allow you to do?",
                "options": {
                    "A": "Define multiple function names",
                    "B": "Accept a variable number of positional arguments",
                    "C": "Create multiple variables at once",
                    "D": "Define default argument values"
                },
                "correct_answer": "B",
                "explanation": "*args allows a function to accept any number of positional arguments as a tuple"
            },
            {
                "question": "What is a list comprehension?",
                "options": {
                    "A": "A way to comment on lists",
                    "B": "A concise way to create lists based on existing lists",
                    "C": "A type of list that doesn't allow modifications",
                    "D": "A method to sort lists"
                },
                "correct_answer": "B",
                "explanation": "List comprehension provides a concise way to create lists: [x*2 for x in range(5)]"
            },
            {
                "question": "What is the purpose of lambda functions?",
                "options": {
                    "A": "Define class methods",
                    "B": "Create anonymous single-expression functions",
                    "C": "Handle exceptions",
                    "D": "Import modules"
                },
                "correct_answer": "B",
                "explanation": "Lambda functions are small anonymous functions defined with: lambda x: x*2"
            },
            {
                "question": "What does the 'with' statement do in Python?",
                "options": {
                    "A": "Creates a database connection",
                    "B": "Properly manages resources like files, ensuring cleanup",
                    "C": "Defines a conditional block",
                    "D": "Imports another module"
                },
                "correct_answer": "B",
                "explanation": "'with' statement ensures proper resource management with automatic cleanup"
            }
        ],
        "advanced": [
            {
                "question": "What is a metaclass in Python?",
                "options": {
                    "A": "A class that creates classes",
                    "B": "A method that starts with 'meta'",
                    "C": "A type of inheritance",
                    "D": "A decorator for classes"
                },
                "correct_answer": "A",
                "explanation": "Metaclasses are classes whose instances are classes. type() is the default metaclass."
            },
            {
                "question": "What is the Global Interpreter Lock (GIL)?",
                "options": {
                    "A": "A security feature that locks your code",
                    "B": "A mutex that prevents multiple threads from executing Python bytecode simultaneously",
                    "C": "A type of database lock",
                    "D": "A feature that optimizes memory usage"
                },
                "correct_answer": "B",
                "explanation": "The GIL ensures that only one thread executes Python bytecode at a time, limiting true parallelism"
            },
            {
                "question": "What does yield do in a generator function?",
                "options": {
                    "A": "Returns and ends the function",
                    "B": "Pauses the function and returns a value, resuming from that point on next call",
                    "C": "Declares a variable",
                    "D": "Imports a module"
                },
                "correct_answer": "B",
                "explanation": "yield pauses execution and returns a value, making functions generators that produce values lazily"
            },
            {
                "question": "What is the difference between deep copy and shallow copy?",
                "options": {
                    "A": "Deep copy is faster",
                    "B": "Shallow copy copies nested objects by reference, deep copy creates independent copies",
                    "C": "They are the same thing",
                    "D": "Deep copy only works for lists"
                },
                "correct_answer": "B",
                "explanation": "Shallow copy copies top level but nested objects share references; deep copy creates completely independent copies"
            },
            {
                "question": "What is decorator in Python?",
                "options": {
                    "A": "A design pattern for decorating objects",
                    "B": "A function that modifies another function or class without changing its source code",
                    "C": "A type of CSS styling",
                    "D": "A way to organize imports"
                },
                "correct_answer": "B",
                "explanation": "Decorators are functions that modify other functions/classes using @decorator syntax"
            }
        ]
    },
    "JavaScript": {
        "beginner": [
            {
                "question": "How do you declare a variable in JavaScript?",
                "options": {
                    "A": "var x = 5;",
                    "B": "let x = 5;",
                    "C": "const x = 5;",
                    "D": "All of the above"
                },
                "correct_answer": "D",
                "explanation": "All three keywords can declare variables, with different scoping and mutability rules"
            },
            {
                "question": "What is the difference between null and undefined?",
                "options": {
                    "A": "They are the same",
                    "B": "null is assigned intentionally, undefined is uninitialized",
                    "C": "undefined is assigned intentionally, null is uninitialized",
                    "D": "null is only for objects"
                },
                "correct_answer": "B",
                "explanation": "null is explicitly assigned to indicate 'no value', undefined means a variable exists but hasn't been assigned"
            },
            {
                "question": "What does console.log() do?",
                "options": {
                    "A": "Logs into a file",
                    "B": "Prints output to the browser console",
                    "C": "Logs errors only",
                    "D": "Creates a file"
                },
                "correct_answer": "B",
                "explanation": "console.log() outputs messages to the browser's developer console for debugging"
            },
            {
                "question": "How do you create a function in JavaScript?",
                "options": {
                    "A": "function myFunc() {}",
                    "B": "def myFunc() {}",
                    "C": "func myFunc() {}",
                    "D": "create myFunc() {}"
                },
                "correct_answer": "A",
                "explanation": "Use 'function' keyword to declare functions in JavaScript"
            },
            {
                "question": "What is an array in JavaScript?",
                "options": {
                    "A": "A single value",
                    "B": "A collection of values in square brackets",
                    "C": "A type of loop",
                    "D": "A function"
                },
                "correct_answer": "B",
                "explanation": "Arrays store multiple values: let arr = [1, 2, 3];"
            }
        ],
        "intermediate": [
            {
                "question": "What is 'this' in JavaScript?",
                "options": {
                    "A": "Always refers to the window",
                    "B": "Always refers to the current object",
                    "C": "Refers to the object the function is called on (context-dependent)",
                    "D": "A keyword that ends the program"
                },
                "correct_answer": "C",
                "explanation": "'this' refers to the object that a method is called on, determined at runtime"
            },
            {
                "question": "What is hoisting in JavaScript?",
                "options": {
                    "A": "Moving values to the top of the code",
                    "B": "The behavior where declarations are moved to the top of their scope",
                    "C": "Deleting variables",
                    "D": "Creating nested objects"
                },
                "correct_answer": "B",
                "explanation": "var and function declarations are hoisted to the top, allowing use before declaration"
            },
            {
                "question": "What is a closure in JavaScript?",
                "options": {
                    "A": "Ending a program",
                    "B": "A function that has access to variables in its outer scope",
                    "C": "A type of loop",
                    "D": "A syntax error"
                },
                "correct_answer": "B",
                "explanation": "A closure allows a function to access variables from its outer scope even after that scope has closed"
            },
            {
                "question": "What is the difference between let and var?",
                "options": {
                    "A": "No difference",
                    "B": "let is block-scoped, var is function-scoped",
                    "C": "var is better than let",
                    "D": "let can't be reassigned"
                },
                "correct_answer": "B",
                "explanation": "let has block scope (inside {}) while var has function scope, let is preferred in modern JavaScript"
            },
            {
                "question": "What do arrow functions do?",
                "options": {
                    "A": "Point to values",
                    "B": "Create a shorthand function syntax with lexical 'this'",
                    "C": "Indicate direction",
                    "D": "They're the same as regular functions"
                },
                "correct_answer": "B",
                "explanation": "Arrow functions (=>) provide concise syntax and don't bind their own 'this'"
            }
        ],
        "advanced": [
            {
                "question": "What is event delegation in JavaScript?",
                "options": {
                    "A": "Creating events manually",
                    "B": "Adding listeners to every element",
                    "C": "Handling events for multiple elements at a parent level using event bubbling",
                    "D": "Preventing events from firing"
                },
                "correct_answer": "C",
                "explanation": "Event delegation attaches one listener to a parent to handle events from many child elements efficiently"
            },
            {
                "question": "What is the difference between map() and forEach()?",
                "options": {
                    "A": "They do the same thing",
                    "B": "map() returns a new array, forEach() doesn't return anything",
                    "C": "forEach() is faster",
                    "D": "map() can only work with numbers"
                },
                "correct_answer": "B",
                "explanation": "map() transforms array elements and returns a new array; forEach() just iterates and doesn't return anything"
            },
            {
                "question": "What is Promise in JavaScript?",
                "options": {
                    "A": "A guarantee that code will run",
                    "B": "An object representing eventual completion of an async operation",
                    "C": "A type of loop",
                    "D": "A variable declaration"
                },
                "correct_answer": "B",
                "explanation": "Promise represents an async operation that will either resolve or reject with a value"
            },
            {
                "question": "What is async/await?",
                "options": {
                    "A": "Keywords for loops",
                    "B": "Syntactic sugar for Promises making async code look synchronous",
                    "C": "A type of error handling",
                    "D": "Functions that are slow"
                },
                "correct_answer": "B",
                "explanation": "async/await makes Promise-based code more readable and easier to work with than .then() chains"
            },
            {
                "question": "What are Symbols in JavaScript?",
                "options": {
                    "A": "Emojis",
                    "B": "Unique identifiers for object properties",
                    "C": "Mathematical symbols",
                    "D": "A type of decorator"
                },
                "correct_answer": "B",
                "explanation": "Symbol creates unique, non-enumerable property keys useful for private object properties"
            }
        ]
    },
    "Java": {
        "beginner": [
            {
                "question": "What is the entry point of a Java application?",
                "options": {
                    "A": "main() method",
                    "B": "start() method",
                    "C": "init() method",
                    "D": "run() method"
                },
                "correct_answer": "A",
                "explanation": "The main() method is the entry point: public static void main(String[] args)"
            },
            {
                "question": "What is the correct syntax for creating a class?",
                "options": {
                    "A": "class MyClass {}",
                    "B": "public class MyClass {}",
                    "C": "Both A and B",
                    "D": "type MyClass {}"
                },
                "correct_answer": "C",
                "explanation": "Both syntaxes are valid; public is optional depending on file structure"
            },
            {
                "question": "What is a variable in Java?",
                "options": {
                    "A": "Always a number",
                    "B": "A named container for storing values",
                    "C": "A function parameter",
                    "D": "A class definition"
                },
                "correct_answer": "B",
                "explanation": "Variables store values of a specific data type and can be accessed by their name"
            },
            {
                "question": "What are the primitive data types in Java?",
                "options": {
                    "A": "int, float, double, boolean",
                    "B": "String, Array, List",
                    "C": "Class, Interface, Object",
                    "D": "byte, short, long, float, double, boolean, char, int"
                },
                "correct_answer": "D",
                "explanation": "Java has 8 primitive types: byte, short, int, long, float, double, boolean, char"
            },
            {
                "question": "How do you create an object in Java?",
                "options": {
                    "A": "new ClassName()",
                    "B": "ClassName()",
                    "C": "create ClassName()",
                    "D": "ClassName object"
                },
                "correct_answer": "A",
                "explanation": "Use the 'new' keyword to instantiate objects: MyClass obj = new MyClass();"
            }
        ],
        "intermediate": [
            {
                "question": "What is inheritance in Java?",
                "options": {
                    "A": "Copying code",
                    "B": "A mechanism where a class extends another class to reuse code",
                    "C": "Creating global variables",
                    "D": "A type of loop"
                },
                "correct_answer": "B",
                "explanation": "Inheritance allows a subclass to inherit properties and methods from a superclass using 'extends'"
            },
            {
                "question": "What is polymorphism?",
                "options": {
                    "A": "Multiple classes",
                    "B": "Multiple objects",
                    "C": "Multiple forms - same method name, different implementations",
                    "D": "Multiple files"
                },
                "correct_answer": "C",
                "explanation": "Polymorphism allows functions/methods to take multiple forms, e.g., method overloading or overriding"
            },
            {
                "question": "What is an interface in Java?",
                "options": {
                    "A": "A visual layout",
                    "B": "A contract defining methods that implementing classes must provide",
                    "C": "A type of class",
                    "D": "A configuration file"
                },
                "correct_answer": "B",
                "explanation": "An interface defines a contract of methods; classes implementing it must provide all methods"
            },
            {
                "question": "What does 'static' mean in Java?",
                "options": {
                    "A": "Doesn't change",
                    "B": "Belongs to the class, not instances; shared by all objects",
                    "C": "Cannot be modified",
                    "D": "Is always visible"
                },
                "correct_answer": "B",
                "explanation": "Static members belong to the class itself, not individual objects, accessible via classname.member"
            },
            {
                "question": "What is the purpose of 'final' keyword?",
                "options": {
                    "A": "Ends a program",
                    "B": "Makes a variable/method/class immutable or prevents overriding",
                    "C": "Marks the last statement",
                    "D": "Declares the end of a block"
                },
                "correct_answer": "B",
                "explanation": "final prevents modification of variables, overriding of methods, or extending of classes"
            }
        ],
        "advanced": [
            {
                "question": "What is a generics in Java?",
                "options": {
                    "A": "Generic properties",
                    "B": "Type-safe way to work with collections without casting",
                    "C": "Generic methods",
                    "D": "Generic classes only"
                },
                "correct_answer": "B",
                "explanation": "Generics enable type-safe collections: List<String> instead of raw List"
            },
            {
                "question": "What is a lambda expression in Java?",
                "options": {
                    "A": "A Greek letter",
                    "B": "Shorthand for anonymous inner classes implementing functional interfaces",
                    "C": "A type of loop",
                    "D": "A variable type"
                },
                "correct_answer": "B",
                "explanation": "Lambda expressions provide concise syntax for functional programming: (x) -> x * 2"
            },
            {
                "question": "What is Stream API in Java?",
                "options": {
                    "A": "Reading files sequentially",
                    "B": "Functional approach to processing collections with map, filter, reduce operations",
                    "C": "A type of loop",
                    "D": "File I/O operations"
                },
                "correct_answer": "B",
                "explanation": "Stream API provides functional-style operations on collections: list.stream().filter().map()"
            },
            {
                "question": "What is reflection in Java?",
                "options": {
                    "A": "Thinking about code",
                    "B": "Ability to examine and modify classes, methods, fields at runtime",
                    "C": "A debugging tool",
                    "D": "A type of error"
                },
                "correct_answer": "B",
                "explanation": "Reflection allows runtime inspection and manipulation of code structure (classes, methods, fields)"
            },
            {
                "question": "What is the purpose of the volatile keyword?",
                "options": {
                    "A": "Makes variables explosion-prone",
                    "B": "Ensures variable changes are visible across threads",
                    "C": "Prevents modification",
                    "D": "Makes variables faster"
                },
                "correct_answer": "B",
                "explanation": "volatile ensures that changes made by one thread are immediately visible to other threads"
            }
        ]
    },
    "React": {
        "beginner": [
            {
                "question": "What is JSX?",
                "options": {
                    "A": "A JavaScript extension for writing HTML-like syntax",
                    "B": "A Java library",
                    "C": "A CSS framework",
                    "D": "A database query language"
                },
                "correct_answer": "A",
                "explanation": "JSX allows writing HTML-like syntax in JavaScript, which gets compiled to React.createElement() calls"
            },
            {
                "question": "What is a React component?",
                "options": {
                    "A": "A piece of UI that can be reused",
                    "B": "A server backend",
                    "C": "A database table",
                    "D": "A CSS stylesheet"
                },
                "correct_answer": "A",
                "explanation": "Components are reusable pieces of UI that encapsulate logic and rendering"
            },
            {
                "question": "What is the difference between state and props?",
                "options": {
                    "A": "They are the same",
                    "B": "props are passed down, state is local to the component",
                    "C": "state is passed down, props are local",
                    "D": "props are for functions, state is for classes"
                },
                "correct_answer": "B",
                "explanation": "Props are inputs passed to components; state is data the component manages internally"
            },
            {
                "question": "How do you update state in React?",
                "options": {
                    "A": "this.state.value = newValue",
                    "B": "this.setState({value: newValue})",
                    "C": "state.value = newValue",
                    "D": "props.setState({value: newValue})"
                },
                "correct_answer": "B",
                "explanation": "Use setState() to update state in class components; never directly modify state"
            },
            {
                "question": "What is the virtual DOM in React?",
                "options": {
                    "A": "A copy of the real DOM in memory",
                    "B": "A JavaScript representation of the actual DOM",
                    "C": "Both A and B",
                    "D": "A database"
                },
                "correct_answer": "C",
                "explanation": "The virtual DOM is an in-memory representation that React uses to optimize actual DOM updates"
            }
        ],
        "intermediate": [
            {
                "question": "What is a React hook?",
                "options": {
                    "A": "A function that lets you use state in functional components",
                    "B": "A type of error handler",
                    "C": "A CSS selector",
                    "D": "A network request"
                },
                "correct_answer": "A",
                "explanation": "Hooks like useState and useEffect enable state and side-effects in functional components"
            },
            {
                "question": "What is the useEffect hook used for?",
                "options": {
                    "A": "Managing side effects in functional components",
                    "B": "Creating styles",
                    "C": "Making API calls only",
                    "D": "Rendering components"
                },
                "correct_answer": "A",
                "explanation": "useEffect runs after render and is used for side effects like API calls, subscriptions, etc."
            },
            {
                "question": "What is the purpose of keys in React lists?",
                "options": {
                    "A": "To unlock features",
                    "B": "To help React identify which items have changed, improving performance",
                    "C": "To encrypt data",
                    "D": "To sort lists"
                },
                "correct_answer": "B",
                "explanation": "Keys help React identify which items have changed/been added/removed, optimizing re-renders"
            },
            {
                "question": "What is lifting state up?",
                "options": {
                    "A": "Physically raising state objects",
                    "B": "Moving shared state to a common ancestor component",
                    "C": "Removing state from components",
                    "D": "Creating global variables"
                },
                "correct_answer": "B",
                "explanation": "Lifting state up moves shared state to a parent component to be shared by multiple children"
            },
            {
                "question": "What is controlled component in React?",
                "options": {
                    "A": "A component that controls other components",
                    "B": "A form element whose value is controlled by React state",
                    "C": "A component that can't be modified",
                    "D": "A parent component"
                },
                "correct_answer": "B",
                "explanation": "Controlled components have their form values managed by React state via onChange handlers"
            }
        ],
        "advanced": [
            {
                "question": "What is React Context?",
                "options": {
                    "A": "The context in which code runs",
                    "B": "A way to pass data through component tree without props drilling",
                    "C": "A debugging tool",
                    "D": "A type of error"
                },
                "correct_answer": "B",
                "explanation": "Context provides a way to pass data to deeply nested components without passing props through every level"
            },
            {
                "question": "What is React Suspense?",
                "options": {
                    "A": "A pause in execution",
                    "B": "A feature for handling code-splitting and async data loading",
                    "C": "A type of error",
                    "D": "A debugging mode"
                },
                "correct_answer": "B",
                "explanation": "Suspense enables managing async operations like lazy loading and data fetching with fallback UI"
            },
            {
                "question": "What is the purpose of useMemo hook?",
                "options": {
                    "A": "To remember errors",
                    "B": "To memoize expensive calculations and prevent unnecessary recalculations",
                    "C": "To store data permanently",
                    "D": "To access memory in the browser"
                },
                "correct_answer": "B",
                "explanation": "useMemo caches computation results and returns the same object reference if dependencies haven't changed"
            },
            {
                "question": "What is render props pattern?",
                "options": {
                    "A": "Props that render HTML",
                    "B": "A pattern where a component receives a function as a prop to render content",
                    "C": "Props for rendering components",
                    "D": "A deprecated feature"
                },
                "correct_answer": "B",
                "explanation": "Render props are functions passed as props that a component calls to determine what to render"
            },
            {
                "question": "What is Higher Order Component (HOC)?",
                "options": {
                    "A": "A component with high height",
                    "B": "A function that takes a component and returns an enhanced component",
                    "C": "A big component",
                    "D": "A type of hook"
                },
                "correct_answer": "B",
                "explanation": "HOC is an advanced pattern for reusing component logic by wrapping components"
            }
        ]
    },
    "SQL": {
        "beginner": [
            {
                "question": "What does SELECT do in SQL?",
                "options": {
                    "A": "Deletes data",
                    "B": "Retrieves data from a table",
                    "C": "Updates data",
                    "D": "Inserts data"
                },
                "correct_answer": "B",
                "explanation": "SELECT retrieves columns from a table: SELECT * FROM table_name;"
            },
            {
                "question": "What is a PRIMARY KEY?",
                "options": {
                    "A": "A key that opens databases",
                    "B": "A unique identifier for each row in a table",
                    "C": "The first column in a table",
                    "D": "A password"
                },
                "correct_answer": "B",
                "explanation": "PRIMARY KEY uniquely identifies each record and ensures no duplicates"
            },
            {
                "question": "What is a FOREIGN KEY?",
                "options": {
                    "A": "A key from another country",
                    "B": "A key that links to the primary key of another table",
                    "C": "A secondary key",
                    "D": "A password for foreign users"
                },
                "correct_answer": "B",
                "explanation": "FOREIGN KEY creates a relationship between two tables by referencing another table's primary key"
            },
            {
                "question": "What does WHERE do in SQL?",
                "options": {
                    "A": "Specifies a location",
                    "B": "Filters rows based on conditions",
                    "C": "Selects all rows",
                    "D": "Joins tables"
                },
                "correct_answer": "B",
                "explanation": "WHERE filters records: SELECT * FROM users WHERE age > 18;"
            },
            {
                "question": "What is a JOIN in SQL?",
                "options": {
                    "A": "Combining two tables",
                    "B": "Combining two tables based on related columns",
                    "C": "A type of loop",
                    "D": "A syntax error"
                },
                "correct_answer": "B",
                "explanation": "JOIN combines rows from two tables based on a related column"
            }
        ],
        "intermediate": [
            {
                "question": "What is the difference between INNER JOIN and LEFT JOIN?",
                "options": {
                    "A": "No difference",
                    "B": "INNER returns matching rows only, LEFT includes all left table rows",
                    "C": "LEFT is faster",
                    "D": "INNER is deprecated"
                },
                "correct_answer": "B",
                "explanation": "INNER JOIN returns only matching records; LEFT JOIN includes all left table records with NULL for non-matches"
            },
            {
                "question": "What is the GROUP BY clause used for?",
                "options": {
                    "A": "Creating groups of users",
                    "B": "Grouping rows by column values for aggregate functions",
                    "C": "Sorting data",
                    "D": "Deleting duplicate rows"
                },
                "correct_answer": "B",
                "explanation": "GROUP BY groups rows by column values for use with aggregate functions like COUNT, SUM, AVG"
            },
            {
                "question": "What is a subquery in SQL?",
                "options": {
                    "A": "A query inside another query",
                    "B": "A query that returns multiple rows",
                    "C": "A type of join",
                    "D": "A backup query"
                },
                "correct_answer": "A",
                "explanation": "A subquery is a query nested inside another query: SELECT * FROM users WHERE id IN (SELECT user_id FROM orders)"
            },
            {
                "question": "What does HAVING do?",
                "options": {
                    "A": "Specifies conditions before filtering",
                    "B": "Specifies conditions on grouped results (like WHERE for GROUP BY)",
                    "C": "Defines table structure",
                    "D": "Creates indexes"
                },
                "correct_answer": "B",
                "explanation": "HAVING filters grouped results: SELECT COUNT(*) FROM users GROUP BY age HAVING COUNT(*) > 5"
            },
            {
                "question": "What is a VIEW in SQL?",
                "options": {
                    "A": "A visual representation",
                    "B": "A virtual table based on a SELECT query",
                    "C": "A type of index",
                    "D": "A user permission"
                },
                "correct_answer": "B",
                "explanation": "A VIEW is a virtual table created from a SELECT query: CREATE VIEW view_name AS SELECT ..."
            }
        ],
        "advanced": [
            {
                "question": "What is database normalization?",
                "options": {
                    "A": "Making databases normal",
                    "B": "Organizing data to reduce redundancy and improve integrity",
                    "C": "Compressing data",
                    "D": "Backing up databases"
                },
                "correct_answer": "B",
                "explanation": "Normalization organizes data into related tables to minimize redundancy and improve data integrity"
            },
            {
                "question": "What is a transaction in SQL?",
                "options": {
                    "A": "A business deal",
                    "B": "A sequence of SQL operations that either all complete or all fail",
                    "C": "A type of query",
                    "D": "A database backup"
                },
                "correct_answer": "B",
                "explanation": "Transaction ensures data consistency: BEGIN; ...statements...; COMMIT; with ROLLBACK on error"
            },
            {
                "question": "What is an INDEX in SQL?",
                "options": {
                    "A": "A list of topics",
                    "B": "A data structure that speeds up data retrieval",
                    "C": "A column number",
                    "D": "A type of query"
                },
                "correct_answer": "B",
                "explanation": "INDEX creates data structures (usually B-trees) to speed up SELECT queries and WHERE clauses"
            },
            {
                "question": "What is the purpose of EXPLAIN in SQL?",
                "options": {
                    "A": "To explain to users",
                    "B": "To show how SQL executes a query (query plan)",
                    "C": "To clarify comments",
                    "D": "To display errors"
                },
                "correct_answer": "B",
                "explanation": "EXPLAIN shows the query execution plan: EXPLAIN SELECT * FROM users WHERE age > 18"
            },
            {
                "question": "What is a CTE (Common Table Expression)?",
                "options": {
                    "A": "A certificate",
                    "B": "A temporary named query useful for recursive queries",
                    "C": "A type of index",
                    "D": "A backup method"
                },
                "correct_answer": "B",
                "explanation": "CTE (WITH clause) creates temporary named result sets: WITH cte AS (SELECT...) SELECT * FROM cte"
            }
        ]
    }
}

FALLBACK_CODING_CHALLENGES = {
    "Python": {
        "basic": [
            {
                "title": "Simple Calculator",
                "description": "Create a simple calculator that takes two numbers and an operation (+, -, *, /) and returns the result.",
                "difficulty": "basic",
                "input_format": "First line: integer a\nSecond line: integer b\nThird line: operation ('+', '-', '*', '/')",
                "output_format": "Result of the operation",
                "constraints": ["a and b between -1000 and 1000", "Operation must be one of: +, -, *, /"],
                "test_cases": [
                    {"input": "5\n3\n+", "expected_output": "8"},
                    {"input": "10\n2\n*", "expected_output": "20"},
                    {"input": "15\n3\n/", "expected_output": "5.0"}
                ],
                "hints": "Use if-elif statements or a dictionary to handle operations"
            }
        ],
        "intermediate": [
            {
                "title": "Find Missing Number",
                "description": "Given an array of n-1 integers containing numbers from 1 to n, find the missing number.",
                "difficulty": "intermediate",
                "input_format": "First line: n\nSecond line: space-separated integers",
                "output_format": "The missing number",
                "constraints": ["1 <= n <= 10000", "Array contains n-1 unique integers from 1 to n"],
                "test_cases": [
                    {"input": "3\n1 2", "expected_output": "3"},
                    {"input": "5\n1 3 4 5", "expected_output": "2"}
                ],
                "hints": "Use the formula n*(n+1)/2 to calculate expected sum, subtract actual sum"
            }
        ],
        "advanced": [
            {
                "title": "Longest Increasing Subsequence",
                "description": "Find the length of the longest increasing subsequence (LIS) in an array.",
                "difficulty": "advanced",
                "input_format": "First line: n\nSecond line: space-separated integers",
                "output_format": "Length of the longest increasing subsequence",
                "constraints": ["1 <= n <= 1000", "values between -10000 and 10000"],
                "test_cases": [
                    {"input": "6\n10 9 2 5 3 7 101 18", "expected_output": "4"},
                    {"input": "4\n3 1 4 1 5", "expected_output": "3"}
                ],
                "hints": "Use dynamic programming with O(n^2) or binary search with O(n log n) approach"
            }
        ]
    },
    "JavaScript": {
        "basic": [
            {
                "title": "String Reversal",
                "description": "Write a function that reverses a string without using built-in reverse() method.",
                "difficulty": "basic",
                "input_format": "A single string",
                "output_format": "The reversed string",
                "constraints": ["String length <= 100", "No built-in reverse() allowed"],
                "test_cases": [
                    {"input": "hello", "expected_output": "olleh"},
                    {"input": "JavaScript", "expected_output": "tpircSavaJ"}
                ],
                "hints": "Use a loop to iterate through the string backwards or convert to array and iterate"
            }
        ],
        "intermediate": [
            {
                "title": "Array Deduplication",
                "description": "Remove duplicate elements from an array while maintaining order.",
                "difficulty": "intermediate",
                "input_format": "Comma-separated integers",
                "output_format": "Deduplicated array as comma-separated values",
                "constraints": ["Array length <= 10000", "Maintain original order"],
                "test_cases": [
                    {"input": "1,2,2,3,3,3,4", "expected_output": "1,2,3,4"},
                    {"input": "5,5,5,5", "expected_output": "5"}
                ],
                "hints": "Use Set, Array.filter(), or reduce() method"
            }
        ],
        "advanced": [
            {
                "title": "Async Promise Chain",
                "description": "Create a promise chain that simulates fetching data from 3 sequential API calls.",
                "difficulty": "advanced",
                "input_format": "User ID (integer)",
                "output_format": "Combined data from all 3 calls",
                "constraints": ["User ID between 1 and 1000", "Proper error handling required"],
                "test_cases": [
                    {"input": "1", "expected_output": "user:{id}|posts:count|comments:count"}
                ],
                "hints": "Use Promise.then() chains or async/await with proper error handling"
            }
        ]
    },
    "Java": {
        "basic": [
            {
                "title": "Factorial Calculator",
                "description": "Calculate the factorial of a given number.",
                "difficulty": "basic",
                "input_format": "An integer n",
                "output_format": "Factorial of n",
                "constraints": ["0 <= n <= 20", "Integer input only"],
                "test_cases": [
                    {"input": "5", "expected_output": "120"},
                    {"input": "0", "expected_output": "1"}
                ],
                "hints": "Use a loop or recursion; factorial(n) = n * (n-1) * ... * 1"
            }
        ],
        "intermediate": [
            {
                "title": "Anagram Checker",
                "description": "Check if two strings are anagrams of each other.",
                "difficulty": "intermediate",
                "input_format": "First line: string1\nSecond line: string2",
                "output_format": "true or false",
                "constraints": ["String length <= 1000", "Case-insensitive comparison"],
                "test_cases": [
                    {"input": "listen\nsilent", "expected_output": "true"},
                    {"input": "hello\nworld", "expected_output": "false"}
                ],
                "hints": "Sort both strings and compare, or count character frequencies"
            }
        ],
        "advanced": [
            {
                "title": "Binary Search Tree Operations",
                "description": "Implement BST insert and search operations.",
                "difficulty": "advanced",
                "input_format": "Operations: INSERT value, SEARCH value",
                "output_format": "Search results",
                "constraints": ["Up to 100 operations", "BST property must be maintained"],
                "test_cases": [
                    {"input": "INSERT 50\nINSERT 30\nINSERT 70\nSEARCH 30", "expected_output": "found"}
                ],
                "hints": "Create a Node class with left and right children, implement recursive insert/search"
            }
        ]
    }
}

def get_mcq_questions(skill: str, proficiency: str = "beginner", count: int = 5):
    """Get MCQ questions for a skill from fallback database"""
    if skill in FALLBACK_MCQ_QUESTIONS:
        if proficiency in FALLBACK_MCQ_QUESTIONS[skill]:
            questions = FALLBACK_MCQ_QUESTIONS[skill][proficiency]
            # Shuffle and return requested count
            import random
            random.shuffle(questions)
            return questions[:count]
    return []

def get_coding_challenges(skill: str):
    """Get coding challenges for a skill"""
    if skill in FALLBACK_CODING_CHALLENGES:
        return FALLBACK_CODING_CHALLENGES[skill]
    return {"basic": [], "intermediate": [], "advanced": []}
