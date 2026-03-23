Title: Development of a Full-Stack Web Calculator with Persistent History

​Objective: Build a responsive web-based calculator using a Frontend (HTML5, CSS3, JavaScript) and a Backend (Node.js or Python) to handle calculation logging and history retrieval.

​1. UI/UX Layout Requirements:
​Display: A top-aligned screen showing both the current input string (e.g., 12 + 45) and the final output.

​Keypad Grid:
​Rows 1-3: Numeric buttons 1–9 arranged in a 3x3 grid.
​Row 4: A = button (left), 0 (middle), and a Delete/Backspace button (right).
​Operator Column: A dedicated fourth column to the right of the numbers containing +, -, *, and / in descending order.
​History Feature: A "History" icon/button in the top-right corner. When clicked, it should toggle a sidebar or modal showing previous calculations.

​2. Functional Logic:
​Two-Digit Resolution: The application must strictly round or truncate all results to exactly two decimal places (e.g., 10 / 3 = 3.33).
​Execution: Calculations should only execute and display a result when the = button is pressed.
​Input Handling: The display must update in real-time as numbers and operators are pressed.

​3. Technical Stack & Backend Integration:
​Frontend: Vanilla JavaScript for DOM manipulation and button event listeners.
​Backend: Create a simple API (using Node.js/Express or Python/Flask) with two endpoints:
​POST /calculate: To send the expression and result to be stored in a local database or JSON file.
​GET /history: To fetch the list of past calculations for the History UI.
​Styling: Use CSS Flexbox/Grid for the layout. Ensure a modern, "App-like" aesthetic with hover states for buttons.