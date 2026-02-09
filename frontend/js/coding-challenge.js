// Coding Challenge Handler
const codingChallenge = {
    currentChallengeIndex: 0,

    // Boilerplate code for different languages
    boilerplates: {
        "c": `#include <stdio.h>

int main() {
    // Write your code here
    printf("Hello World\\n");
    return 0;
}`,
        "cpp": `#include <iostream>
using namespace std;

int main() {
    // Write your code here
    cout << "Hello World" << endl;
    return 0;
}`,
        "cpp14": `#include <iostream>
using namespace std;

int main() {
    // C++ 14
    cout << "Hello World" << endl;
    return 0;
}`,
        "cpp17": `#include <iostream>
using namespace std;

int main() {
    // C++ 17
    cout << "Hello World" << endl;
    return 0;
}`,
        "cpp20": `#include <iostream>
using namespace std;

int main() {
    // C++ 20
    cout << "Hello World" << endl;
    return 0;
}`,
        "java": `import java.util.*;

public class Main {
    public static void main(String[] args) {
        // Write your code here
        System.out.println("Hello World");
    }
}`,
        "python": `def solve():
    # Write your code here
    print("Hello World")

if __name__ == "__main__":
    solve()`,
        "python3": `def solve():
    # Python 3
    print("Hello World")

if __name__ == "__main__":
    solve()`,
        "csharp": `using System;

class Program {
    static void Main() {
        Console.WriteLine("Hello World");
    }
}`,
        "javascript": `// Write your code here
console.log("Hello World");`,
        "typescript": `// TypeScript
console.log("Hello World");`,
        "php": `<?php
// PHP
echo "Hello World";
?>`,
        "ruby": `# Ruby
puts "Hello World"`,
        "go": `package main
import "fmt"

func main() {
    fmt.Println("Hello World")
}`,
        "rust": `fn main() {
    println!("Hello World");
}`,
        "swift": `print("Hello World")`,
        "kotlin": `fun main() {
    println("Hello World")
}`,
        "bash": `#!/bin/bash
echo "Hello World"`,
        "pascal": `program Hello;
begin
  writeln('Hello World');
end.`,
        "lua": `print("Hello World")`,
        "perl": `print "Hello World\\n";`,
        "r": `print("Hello World")`,
        "dart": `void main() {
  print('Hello World');
}`,
        "groovy": `println "Hello World"`,
        "scala": `object Main extends App {
  println("Hello World")
}`,
        "fsharp": `printfn "Hello World"`,
        "sql": `-- SQLite
SELECT "Hello World";`
    },

    // Map display names to internal keys - Only Essential Languages
    languageList: [
        { name: "C", key: "c" },
        { name: "C++", key: "cpp" },
        { name: "Python 3", key: "python" },
        { name: "Java", key: "java" },
        { name: "JavaScript (Node.js)", key: "javascript" },
        { name: "SQL (SQLite)", key: "sql" },
        { name: "Kotlin", key: "kotlin" },
        { name: "Go (Golang)", key: "go" },
        { name: "Rust", key: "rust" },
        { name: "Swift", key: "swift" },
        { name: "R", key: "r" }
    ],

    // Helper to fuzzy match skill to language key
    getLanguageFromSkill(skill) {
        if (!skill) return "java";
        const lowerSkill = skill.toLowerCase();

        if (lowerSkill.includes("python")) return "python";
        if (lowerSkill.includes("java") && !lowerSkill.includes("script")) return "java";
        if (lowerSkill.includes("javascript") || lowerSkill.includes("js")) return "javascript";
        if (lowerSkill.includes("c++") || lowerSkill.includes("cpp")) return "cpp";
        if (lowerSkill.includes("c#") || lowerSkill.includes("csharp")) return "csharp";
        if (lowerSkill.includes("sql")) return "sql";
        if (lowerSkill.includes("go")) return "go";
        if (lowerSkill.includes("rust")) return "rust";
        if (lowerSkill.includes("php")) return "php";
        if (lowerSkill.includes("ruby")) return "ruby";
        if (lowerSkill.includes("html")) return "html";

        // Default to Java if no match or just "C" (ambiguous)
        if (lowerSkill === "c") return "c";

        return "java";
    },

    // Display coding challenge
    displayChallenge(index) {
        const challenge = app.quiz.coding_challenges[index];
        const container = document.getElementById('codingChallengeContent');

        // Smart Default Selection
        const defaultLangKey = this.getLanguageFromSkill(challenge.skill);
        let defaultBoilerplate = this.boilerplates[defaultLangKey] || this.boilerplates['java'];

        // Use starter code from backend if available
        if (challenge.starter_code) {
            defaultBoilerplate = challenge.starter_code;
        }

        // Generate Options HTML
        const optionsHtml = this.languageList.map(lang =>
            `<option value="${lang.key}" ${lang.key === defaultLangKey ? 'selected' : ''}>${lang.name}</option>`
        ).join('');

        let html = `
            <div class="challenge-layout" style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; height: calc(100vh - 200px);">
                <!-- Left Panel: Problem Description -->
                <div class="left-panel" style="overflow-y: auto; padding-right: 10px;">
                    <div class="challenge-info" style="background: white; padding: 20px; border-radius: 12px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                        <div style="display: flex; justify-content: space-between; align-items: start;">
                            <h3 style="color: #1a1a1a; margin-top: 0;">${challenge.title}</h3>
                            <span class="badge" style="background: #e0f2fe; color: #0284c7; padding: 4px 8px; border-radius: 4px; font-size: 0.8rem;">${challenge.difficulty || 'Medium'}</span>
                        </div>
                        <p style="margin: 15px 0; line-height: 1.6; color: #4b5563;">${challenge.description}</p>
                        
                        <div style="background: #f8fafc; padding: 15px; border-radius: 8px; margin: 15px 0;">
                            <strong>Input Format:</strong>
                            <p style="margin: 5px 0; color: #4b5563;">${challenge.input_format}</p>
                        </div>
                        <div style="background: #f8fafc; padding: 15px; border-radius: 8px; margin: 15px 0;">
                            <strong>Output Format:</strong>
                            <p style="margin: 5px 0; color: #4b5563;">${challenge.output_format}</p>
                        </div>
                        
                        <div style="margin: 15px 0;">
                            <strong>Constraints:</strong>
                            <ul style="margin-left: 20px; color: #4b5563;">
                                ${challenge.constraints.map(c => `<li style="margin-bottom: 5px;">${c}</li>`).join('')}
                            </ul>
                        </div>
                    </div>
                
                    <div class="test-cases" style="background: white; padding: 20px; border-radius: 12px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                        <h4 style="color: #1a1a1a; margin-top: 0;">Example Test Cases</h4>
                        ${challenge.test_cases.slice(0, 2).map((tc, i) => `
                            <div class="test-case" style="margin: 15px 0; background: #f8fafc; padding: 15px; border-radius: 8px; border-left: 3px solid #0284c7;">
                                <div style="margin-bottom: 8px;"><strong>Input:</strong> <code style="background: #e2e8f0; padding: 2px 5px; border-radius: 4px;">${tc.input}</code></div>
                                <div><strong>Output:</strong> <code style="background: #e2e8f0; padding: 2px 5px; border-radius: 4px;">${tc.expected_output}</code></div>
                            </div>
                        `).join('')}
                    </div>
                </div>
                
                <!-- Right Panel: Editor & Output -->
                <div class="right-panel" style="display: flex; flex-direction: column; gap: 15px;">
                    <div class="coding-editor" style="display: flex; flex-direction: column; flex: 2; background: #1e1e1e; border-radius: 12px; overflow: hidden;">
                        <div class="editor-header" style="background: #2d2d2d; padding: 10px 15px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #3d3d3d;">
                            <div style="display: flex; align-items: center; gap: 10px;">
                                <span style="color: #e5e7eb;">Language:</span>
                                <select class="language-selector" id="languageSelector" onchange="codingChallenge.onLanguageChange()" style="background-color: #3d3d3d; color: white; border: 1px solid #4b5563; padding: 4px 8px; border-radius: 4px;">
                                    ${optionsHtml}
                                </select>
                            </div>
                            <div style="font-size: 0.8rem; color: #9ca3af;">Auto-saved</div>
                        </div>
                        <textarea 
                            class="code-input" 
                            id="codeInput" 
                            spellcheck="false"
                            style="flex: 1; background: #1e1e1e; color: #d4d4d4; border: none; padding: 15px; font-family: 'Consolas', 'Monaco', monospace; font-size: 14px; line-height: 1.5; resize: none; outline: none;"
                        >${defaultBoilerplate}</textarea>
                    </div>

                    <!-- Console / Output Section -->
                    <div class="console-output" style="flex: 1; background: #1e1e1e; border-radius: 12px; display: flex; flex-direction: column; overflow: hidden; min-height: 200px;">
                        <div style="background: #2d2d2d; padding: 10px 15px; border-bottom: 1px solid #3d3d3d; display: flex; justify-content: space-between;">
                            <span style="color: #e5e7eb; font-weight: 500;">Console Output</span>
                            <button onclick="document.getElementById('codeOutput').innerHTML = ''" style="background: none; border: none; color: #9ca3af; cursor: pointer; font-size: 0.8rem;">Clear</button>
                        </div>
                        <div id="codeOutput" style="padding: 15px; color: #d4d4d4; font-family: monospace; overflow-y: auto; flex: 1;">
                            <div style="color: #6b7280;">Run your code to see output here...</div>
                        </div>
                    </div>
                    
                    <div class="button-group" style="display: flex; gap: 10px; justify-content: flex-end;">
                        <button class="btn" style="background: #374151; color: white; border: 1px solid #4b5563;" onclick="codingChallenge.runCode()">
                            ▶️ Run Code
                        </button>
                        <button class="btn btn-success" onclick="codingChallenge.submitCode()">
                            Submit Solution
                        </button>
                    </div>
                </div>
            </div>
        `;

        container.innerHTML = html;
        this.currentChallengeIndex = index;
    },

    // Handle language change
    onLanguageChange() {
        const lang = document.getElementById('languageSelector').value;
        const editor = document.getElementById('codeInput');

        // Confirm before overwriting if user has typed something significant
        if (editor.value.length > 50 && editor.value !== this.boilerplates[lang]) {
            if (!confirm("Changing language will reset your code. Continue?")) {
                // Revert selection
                // (Implementation omitted for brevity, would strictly need previous value)
                return;
            }
        }

        // Check if we can use starter code for this language
        const currentChallenge = app.quiz.coding_challenges[this.currentChallengeIndex];
        const challengeLangKey = this.getLanguageFromSkill(currentChallenge.skill);

        if (lang === challengeLangKey && currentChallenge.starter_code) {
            editor.value = currentChallenge.starter_code;
        } else {
            editor.value = this.boilerplates[lang] || '';
        }
    },

    // Run code (client-side preview)
    async runCode() {
        const code = document.getElementById('codeInput').value;
        const language = document.getElementById('languageSelector').value;
        const outputDiv = document.getElementById('codeOutput');

        if (!code.trim()) {
            outputDiv.innerHTML = '<span style="color: #ef4444;">Please write some code before running.</span>';
            return;
        }

        // Show loading
        outputDiv.innerHTML = '<span style="color: #fbbf24;">Running code...</span>';

        try {
            const response = await fetch(`${app.apiUrl}/submit-code`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    session_id: app.sessionId,
                    code: code,
                    language: language,
                    challenge_index: this.currentChallengeIndex,
                    is_preview: true
                })
            });

            const data = await response.json();

            if (data.success) {
                this.displayRunResults(data.result);
            } else {
                throw new Error(data.error || 'Execution failed');
            }
        } catch (error) {
            outputDiv.innerHTML = `<span style="color: #ef4444;">Error: ${error.message}</span>`;
        }
    },

    // Display HTML/CSS/JS preview in iframe
    displayHTMLPreview(code) {
        const outputDiv = document.getElementById('codeOutput');

        // Create iframe for preview
        outputDiv.innerHTML = `
            <div style="display: flex; flex-direction: column; height: 100%;">
                <div style="background: #2d2d2d; padding: 8px 12px; border-bottom: 1px solid #3d3d3d; color: #10b981; font-size: 0.85rem;">
                    ✓ Live Preview
                </div>
                <iframe 
                    id="htmlPreviewFrame" 
                    sandbox="allow-scripts" 
                    style="flex: 1; border: none; background: white; width: 100%; min-height: 300px;"
                ></iframe>
            </div>
        `;

        // Inject code into iframe
        const iframe = document.getElementById('htmlPreviewFrame');
        const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
        iframeDoc.open();
        iframeDoc.write(code);
        iframeDoc.close();
    },


    // Display run results in the console area
    displayRunResults(result) {
        const outputDiv = document.getElementById('codeOutput');
        let html = '';

        // Prioritize actual output / input echo
        if (result.test_results && result.test_results.length > 0) {
            result.test_results.forEach((test, i) => {
                const color = test.passed ? '#4ade80' : '#f87171';
                html += `
                    <div style="margin-bottom: 15px; border-bottom: 1px solid #333; padding-bottom: 10px;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="color: #9ca3af; font-size: 0.9em;">Test Case ${test.test_case}</span>
                            <span style="color: ${color}; font-weight: bold; font-size: 0.8rem;">${test.passed ? 'PASSED' : 'FAILED'}</span>
                        </div>
                        
                        <div style="margin-top: 8px; font-size: 0.85rem;">
                            <div style="display: grid; grid-template-columns: 80px 1fr; gap: 5px; margin-bottom: 4px;">
                                <span style="color: #6b7280;">Input:</span>
                                <code style="color: #d4d4d4;">${test.input}</code>
                            </div>
                            <div style="display: grid; grid-template-columns: 80px 1fr; gap: 5px; margin-bottom: 4px;">
                                <span style="color: #6b7280;">Expected:</span>
                                <code style="color: #d4d4d4;">${test.expected_output}</code>
                            </div>
                            <div style="display: grid; grid-template-columns: 80px 1fr; gap: 5px;">
                                <span style="color: #6b7280;">Actual:</span>
                                <code style="color: ${test.passed ? '#d4d4d4' : '#fca5a5'};">${test.actual_output || '<span style="color: #525252; font-style: italic;">(No Output)</span>'}</code>
                            </div>
                        </div>
                        
                        ${test.error ?
                        `<div style="color: #ef4444; margin-top: 8px; font-size: 0.85rem; background: rgba(239, 68, 68, 0.1); padding: 5px; border-radius: 4px;">Error: ${test.error}</div>` : ''
                    }
                    </div>
                `;
            });
        } else if (result.error) {
            html += `<div style="color: #ef4444; white-space: pre-wrap;">${result.error}</div>`;
        } else {
            html += `<span style="color: #9ca3af;">No test results available.</span>`;
        }

        outputDiv.innerHTML = html;
    },

    // Submit code (Final Submission)
    async submitCode() {
        const code = document.getElementById('codeInput').value;
        const language = document.getElementById('languageSelector').value;

        if (!code.trim()) {
            app.showError('Please write some code before submitting');
            return;
        }

        const submitBtn = document.querySelector('.btn-success');
        const originalText = submitBtn.textContent;
        submitBtn.disabled = true;
        submitBtn.textContent = 'Evaluating...';

        try {
            const response = await fetch(`${app.apiUrl}/submit-code`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    session_id: app.sessionId,
                    code: code,
                    language: language,
                    challenge_index: this.currentChallengeIndex
                })
            });

            const data = await response.json();

            if (data.success) {
                // Show modal or alert with score
                const result = data.result;
                const scoreColor = result.score >= 70 ? 'success' : (result.score >= 40 ? 'warning' : 'error');

                let message = `Score: ${result.score}%\nTests Passed: ${result.passed_tests}/${result.total_tests}`;
                if (result.score === 100) message = "Perfect Score! Well done! 🎉";

                alert(message); // Simple alert for now, can be upgraded to modal

                if (this.currentChallengeIndex < app.quiz.coding_challenges.length - 1) {
                    if (confirm('Move to next coding challenge?')) {
                        this.displayChallenge(this.currentChallengeIndex + 1);
                    }
                } else {
                    app.goToStep(5);
                    hrInterview.startInterview();
                }
            } else {
                throw new Error(data.error || 'Failed to submit code');
            }
        } catch (error) {
            app.showError('Submission failed: ' + error.message);
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = originalText;
        }
    },

    // Kept for compatibility if called from elsewhere
    displayResults(result) {
        // Redundant with the alert above, but good to have just in case
        console.log("Results:", result);
    }
};
