import { marked } from 'marked';
marked.use({
    renderer: {
        link(token) {
            console.log(token);
            return `<a href="${token.href}">${token.text}</a>`;
        }
    }
});
console.log(marked.parse('[hello](world.jpg)'));
