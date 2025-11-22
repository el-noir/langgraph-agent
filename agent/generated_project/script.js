(function () {
    'use strict';

    // State variables
    let currentInput = '';
    let result = null;

    // DOM references
    const displayEl = document.getElementById('display');
    const buttons = document.querySelectorAll('.btn');

    // Utility: update the calculator display
    function updateDisplay() {
        if (currentInput !== '') {
            displayEl.textContent = currentInput;
        } else if (result !== null) {
            displayEl.textContent = result;
        } else {
            displayEl.textContent = '';
        }
    }

    // Utility: clear all entries
    function clearAll() {
        currentInput = '';
        result = null;
        updateDisplay();
    }

    // Utility: remove last character
    function backspace() {
        if (currentInput.length > 0) {
            currentInput = currentInput.slice(0, -1);
            updateDisplay();
        }
    }

    // Utility: append a character after validation
    function appendCharacter(char) {
        const allowed = /^[0-9+\-*/().]$/;
        if (!allowed.test(char)) return;

        // Prevent multiple consecutive operators (except minus for negative numbers)
        const operators = '+-*/';
        const lastChar = currentInput.slice(-1);
        if (operators.includes(char) && operators.includes(lastChar) && !(char === '-' && lastChar !== '-')) {
            // Replace the last operator with the new one
            currentInput = currentInput.slice(0, -1) + char;
        } else {
            currentInput += char;
        }
        updateDisplay();
    }

    // Utility: evaluate the current expression safely
    function evaluateExpression() {
        if (currentInput.trim() === '') return;

        // Sanitize: allow only digits, decimal point, parentheses and basic operators
        const sanitized = currentInput.replace(/[^0-9+\-*/().]/g, '');

        // Detect division by zero (simple pattern)
        if (/\/0(?!\d)/.test(sanitized)) {
            result = 'Error';
            currentInput = '';
            updateDisplay();
            return;
        }

        try {
            // Use Function constructor for evaluation
            const evalResult = Function('return ' + sanitized)();
            if (evalResult === Infinity || evalResult === -Infinity || Number.isNaN(evalResult)) {
                result = 'Error';
            } else {
                result = Number.isFinite(evalResult) ? evalResult : 'Error';
            }
        } catch (e) {
            result = 'Error';
        }

        currentInput = (result !== 'Error') ? String(result) : '';
        updateDisplay();
    }

    // Central input handler
    function handleInput(val) {
        switch (val) {
            case 'C':
                clearAll();
                break;
            case '←':
                backspace();
                break;
            case '=':
                evaluateExpression();
                break;
            default:
                appendCharacter(val);
                break;
        }
    }

    // Attach click listeners to buttons
    buttons.forEach(btn => {
        btn.addEventListener('click', () => {
            const val = btn.dataset.value;
            if (val) handleInput(val);
        });
    });

    // Keyboard handling
    document.addEventListener('keydown', e => {
        const keyMap = {
            'Enter': '=',
            '=': '=',
            'Backspace': '←',
            'Escape': 'C',
            'c': 'C',
            'C': 'C',
            '+': '+',
            '-': '-',
            '*': '*',
            '/': '/',
            '.': '.',
            '(': '(',
            ')': ')',
            '0': '0',
            '1': '1',
            '2': '2',
            '3': '3',
            '4': '4',
            '5': '5',
            '6': '6',
            '7': '7',
            '8': '8',
            '9': '9'
        };

        if (e.key in keyMap) {
            e.preventDefault(); // prevent form submission / navigation
            handleInput(keyMap[e.key]);
        }
    });

    // Initial display update
    updateDisplay();

    // Optional export for testing
    window.calculator = {
        clearAll,
        backspace,
        appendCharacter,
        evaluateExpression,
        getCurrentInput: () => currentInput,
        getResult: () => result
    };
})();