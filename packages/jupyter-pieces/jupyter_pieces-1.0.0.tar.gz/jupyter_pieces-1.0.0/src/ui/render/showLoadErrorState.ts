import { addLogo } from './addLogo';
import { theme } from '../../index';

export function showLoadErrorState(container: HTMLElement) {
    container.innerHTML = '';

    addLogo(container);
    container.classList.add('load-error-state');

    let line1 = document.createElement('p');
    line1.innerText =
        "Oops! We couldn't access your snippets. Something went wrong. Please make sure Pieces OS is installed, updated, and running.";
    container.appendChild(line1);

    let installButton = document.createElement('button');
    installButton.classList.add('jp-btn');
    installButton.innerText = 'Install Platform Core';
    installButton.addEventListener('click', function () {
        window.open('https://pieces.app/', '_blank');
    });
    container.appendChild(installButton);

    let line2 = document.createElement('p');
    line2.innerText = 'Or...';
    container.appendChild(line2);

    let launchButton = document.createElement('button');
    launchButton.classList.add('jp-btn');
    launchButton.innerText = 'Launch Pieces OS';
    launchButton.addEventListener('click', function () {
        console.log('Launching Pieces OS...');
        window.open('pieces://launch', '_blank');
    });
    container.appendChild(launchButton);

    let line3 = document.createElement('p');
    line3.innerHTML = `Please refresh after launching PiecesOS. If the problem persists, please `;
    let underline = document.createElement('u');
    underline.innerText = 'see our FAQ.';
    let link = document.createElement('a');
    link.href = 'https://docs.pieces.app/faq';
    link.target = '_blank';
    link.appendChild(underline);
    line3.appendChild(link);
    container.appendChild(line3);

    let illustration = document.createElement('div');
    illustration.classList.add('illustration');
    if (theme === 'false') {
        illustration.classList.add('illustration-robot-plugging-in-black');
    }
    else {
        illustration.classList.add('illustration-robot-plugging-in-white');
    }
    container.appendChild(illustration);
}
