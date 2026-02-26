// Generate with prompt - Opens Gemini and copies prompt to clipboard
window.generateWithPrompt = function (promptText) {
    console.log('🎨 Opening Gemini for prompt:', promptText);

    // Optimize prompt for coloring book
    const optimizedPrompt = `${promptText}, coloring book style, black and white line art, simple outlines, no shading, clean lines, white background, suitable for children`;

    // Copy to clipboard first
    navigator.clipboard.writeText(optimizedPrompt).then(() => {
        console.log('✅ Prompt copied to clipboard');

        // Detect mobile device
        const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);

        if (isMobile) {
            // Mobile: Try to open Gemini app with deep link
            const appUrl = 'gemini://chat';
            const webUrl = 'https://gemini.google.com/app';

            window.location.href = appUrl;

            setTimeout(() => {
                window.open(webUrl, '_blank');
            }, 1000);

            showToast('✅ Prompt copied! Paste it in Gemini (opening...)', 4000);
        } else {
            // Desktop: Open Gemini web
            const geminiUrl = 'https://gemini.google.com/app';
            const newTab = window.open(geminiUrl, '_blank');

            if (!newTab) {
                alert('Popup blocked! Enable popups.\n\nPrompt copied to clipboard: ' + optimizedPrompt);
            } else {
                showToast('✅ Prompt copied! Paste it in Gemini (new tab opened)', 4000);
            }
        }
    }).catch(err => {
        console.error('Failed to copy:', err);
        alert('Prompt: ' + optimizedPrompt);
    });
};

console.log('✅ Gemini redirect loaded (clipboard + tab)');
