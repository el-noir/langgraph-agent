# SimpleCalculator

A lightweight web‑based calculator that performs basic arithmetic operations. It runs entirely in the browser with no build steps or server dependencies.

## Tech Stack
- **HTML**
- **CSS**
- **JavaScript**

## Setup
1. Clone the repository  
   ```bash
   git clone https://github.com/yourusername/simple-calculator.git
   cd simple-calculator
   ```
2. Open `index.html` in any modern web browser.  
   No additional installation or build steps are required.

## Usage Guide
- **Button Layout** – The interface mimics a classic handheld calculator:
  - Digits `0‑9` and decimal point `.` are centered at the bottom.
  - Basic operators `+`, `-`, `*`, `/` are placed on the right side.
  - `=` evaluates the current expression.
  - `C` clears the display.
  - `←` (Backspace) deletes the last character.
- **Mouse Interaction** – Click any button to input the corresponding character or command.
- **Keyboard Shortcuts**  
  - Numbers `0‑9` and `.` type directly.  
  - `+`, `-`, `*`, `/` map to their respective operations.  
  - `Enter` → `=` (evaluate).  
  - `Backspace` → `←` (delete last entry).  
  - `Esc` → `C` (clear).  
- **Responsive Behavior** – The layout scales gracefully on mobile devices; buttons enlarge for touch input and the calculator fits within the viewport width.

## Development Notes
### File Responsibilities
- **`index.html`** – Defines the calculator UI, imports the stylesheet and script, and provides the container for the display and buttons.
- **`styles.css`** – Contains all visual styling, including layout, colors, responsive breakpoints, and button states.
- **`script.js`** – Implements the calculator logic, handling user input, updating the display, and performing calculations.

### Core `script.js` Functions & Variables
| Symbol | Description |
|--------|-------------|
| `displayElement` | Reference to the `<div>` that shows the current expression/result. |
| `currentExpression` | String that accumulates user input (e.g., `"12+7"`). |
| `append(char)` | Adds a character (digit, operator, or decimal) to `currentExpression` and refreshes the display. |
| `clearDisplay()` | Resets `currentExpression` to an empty string and clears the display. |
| `deleteLast()` | Removes the last character from `currentExpression`. |
| `evaluateExpression()` | Safely evaluates `currentExpression` using `Function` constructor, handling errors and updating the display with the result. |
| `handleButtonClick(event)` | Delegates click events from calculator buttons to the appropriate function. |
| `handleKeyPress(event)` | Maps keyboard keys to calculator actions (numbers, operators, Enter, Backspace, Esc). |
| `init()` | Sets up event listeners for button clicks and keyboard input; called on script load. |

### Extending Functionality
- **Parentheses** – Add `(` and `)` buttons, update `append` validation to allow balanced parentheses, and ensure `evaluateExpression` can parse them.
- **Scientific Operations** – Introduce functions like `sin`, `cos`, `log`, etc., by expanding the button set and extending `evaluateExpression` with a whitelist of `Math` methods.
- **Theme Switching** – Implement CSS variables for colors and a toggle button that swaps light/dark themes via JavaScript.

## License
[Insert License Here]