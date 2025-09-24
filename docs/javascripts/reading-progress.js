// 阅读进度条和增强功能
document.addEventListener('DOMContentLoaded', function() {
    
    // 创建进度条
    const progressBar = document.createElement('div');
    progressBar.className = 'reading-progress';
    document.body.appendChild(progressBar);
    
    // 创建章节进度指示器
    const chapterProgress = document.createElement('div');
    chapterProgress.className = 'chapter-progress';
    document.body.appendChild(chapterProgress);
    
    // 更新阅读进度
    function updateProgress() {
        const scrollTop = window.pageYOffset;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        const progress = (scrollTop / docHeight) * 100;
        
        progressBar.style.width = progress + '%';
        chapterProgress.textContent = Math.round(progress) + '%';
    }
    
    // 懒加载图片
    function lazyLoadImages() {
        const images = document.querySelectorAll('img[data-src]');
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.setAttribute('data-loaded', 'true');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    }
    
    // 键盘导航
    document.addEventListener('keydown', function(e) {
        if (e.target.tagName === 'INPUT') return;
        
        if (e.key === 'ArrowLeft') {
            const prevLink = document.querySelector('a[title*="Previous"]');
            if (prevLink) prevLink.click();
        } else if (e.key === 'ArrowRight') {
            const nextLink = document.querySelector('a[title*="Next"]');
            if (nextLink) nextLink.click();
        }
    });
    
    // 搜索建议功能
    function enhanceSearch() {
        const searchInput = document.querySelector('input[type="search"]');
        if (!searchInput) return;
        
        const suggestions = ['刷酸', '护肤', '酸类', '浓度', '敏感肌', '痘痘', '美白', '抗老'];
        
        searchInput.addEventListener('input', function() {
            const value = this.value.toLowerCase();
            if (value.length < 2) return;
            
            const matches = suggestions.filter(s => s.includes(value));
            showSuggestions(matches, this);
        });
    }
    
    function showSuggestions(suggestions, input) {
        let container = document.querySelector('.search-suggestions');
        if (!container) {
            container = document.createElement('div');
            container.className = 'search-suggestions';
            input.parentNode.appendChild(container);
        }
        
        container.innerHTML = suggestions.map(s => 
            `<div class="search-suggestion">${s}</div>`
        ).join('');
        
        container.querySelectorAll('.search-suggestion').forEach(item => {
            item.addEventListener('click', () => {
                input.value = item.textContent;
                container.remove();
            });
        });
    }
    
    // 初始化功能
    window.addEventListener('scroll', updateProgress);
    lazyLoadImages();
    enhanceSearch();
    updateProgress();
});
