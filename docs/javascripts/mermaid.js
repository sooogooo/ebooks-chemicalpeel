// Mermaid configuration for MkDocs Material theme
document$.subscribe(() => {
  mermaid.initialize({
    startOnLoad: true,
    theme: 'default',
    themeVariables: {
      primaryColor: '#7FB069',
      primaryTextColor: '#2C3E50',
      primaryBorderColor: '#5A8A4A',
      lineColor: '#666666',
      secondaryColor: '#E8B4B8',
      tertiaryColor: '#F4E4C1',
      background: '#ffffff',
      mainBkg: '#ffffff',
      secondBkg: '#f8f9fa',
      tertiaryBkg: '#f1f3f4'
    },
    flowchart: {
      useMaxWidth: true,
      htmlLabels: true,
      curve: 'basis'
    },
    sequence: {
      diagramMarginX: 50,
      diagramMarginY: 10,
      actorMargin: 50,
      width: 150,
      height: 65,
      boxMargin: 10,
      boxTextMargin: 5,
      noteMargin: 10,
      messageMargin: 35,
      mirrorActors: true,
      bottomMarginAdj: 1,
      useMaxWidth: true,
      rightAngles: false,
      showSequenceNumbers: false
    },
    gantt: {
      titleTopMargin: 25,
      barHeight: 20,
      fontFamily: '"Noto Sans SC", Arial, sans-serif',
      fontSize: 11,
      fontWeight: 'normal',
      gridLineStartPadding: 35,
      bottomPadding: 5,
      leftPadding: 75,
      topPadding: 50,
      rightPadding: 25
    }
  });
});

// Re-initialize Mermaid when content changes (for SPA navigation)
document.addEventListener('DOMContentLoaded', function() {
  const observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
      if (mutation.type === 'childList') {
        const mermaidElements = document.querySelectorAll('.mermaid');
        if (mermaidElements.length > 0) {
          mermaid.init(undefined, mermaidElements);
        }
      }
    });
  });
  
  observer.observe(document.body, {
    childList: true,
    subtree: true
  });
});
