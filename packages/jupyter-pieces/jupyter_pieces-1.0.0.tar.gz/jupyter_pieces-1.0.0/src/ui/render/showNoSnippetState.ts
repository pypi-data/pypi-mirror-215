import { constructSnippet } from '../views/renderListView';
import { addLogo } from './addLogo';

export function showNoSnippetState(container: HTMLDivElement) {
    container.innerHTML = '';

    let stateContainer = document.createElement('div');
    stateContainer.classList.add('pieces-empty-state');

    addLogo(stateContainer);

    let firstLine = document.createElement('p');
    firstLine.innerText =
        "You're so close to getting started! Try saving this code snippet!";
    stateContainer.appendChild(firstLine);

    let snippetConstraint = document.createElement('div');
    snippetConstraint.classList.add('snippetConstraint');

    //Switch out this stringified Piece code for new JSON if you want to change the default snippet
    const testPieceData = `{"title":"Class HelloWorld","id":"457891fd-d363-460d-bdb6-32149a1131c2","type":"CODE","raw":"class HelloWorld:\\n    def __init__(self):\\n        self.message = \\"Hello, World!\\"\\n\\n    def say_hello(self):\\n        print(self.message)\\n\\n# Create an instance of the class\\nhello = HelloWorld()\\n\\n# Call the say_hello method\\nhello.say_hello()","language":"py","time":"2 minutes ago","created":"2023-06-12T15:57:01.493Z","description":"📝 Custom Description: \\nWrite a custom description here.\\n\\n💡 Smart Description: \\nThis code generates a class called \\"Hello\\" with the value of 0.\\n\\n🔎 Suggested Searches: \\nHow to create a class with message ?\\nHow to add the new instance of HelloWorld?\\nWhat is the syntax for creating a class  using Snowflake script ?"}`;
    let testPiece = constructSnippet(JSON.parse(testPieceData), true);
    snippetConstraint.appendChild(testPiece);

    container.appendChild(stateContainer);
    container.appendChild(snippetConstraint);
}
