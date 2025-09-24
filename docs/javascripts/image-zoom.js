// 图片缩放功能
(function() {
    let modal = null;
    let currentImg = null;
    let scale = 1;
    
    function createModal() {
        modal = document.createElement('div');
        modal.style.cssText = `
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.9); z-index: 9999; display: none;
            justify-content: center; align-items: center; cursor: zoom-out;
        `;
        
        const img = document.createElement('img');
        img.style.cssText = `
            max-width: 90%; max-height: 90%; transition: transform 0.3s;
            cursor: grab;
        `;
        
        const controls = document.createElement('div');
        controls.style.cssText = `
            position: absolute; top: 20px; right: 20px; color: white;
        `;
        controls.innerHTML = `
            <button onclick="zoomIn()" style="margin-right: 10px; padding: 5px 10px; background: rgba(255,255,255,0.2); color: white; border: none; cursor: pointer;">+</button>
            <button onclick="zoomOut()" style="margin-right: 10px; padding: 5px 10px; background: rgba(255,255,255,0.2); color: white; border: none; cursor: pointer;">-</button>
            <button onclick="closeModal()" style="padding: 5px 10px; background: rgba(255,255,255,0.2); color: white; border: none; cursor: pointer;">×</button>
        `;
        
        modal.appendChild(img);
        modal.appendChild(controls);
        document.body.appendChild(modal);
        
        currentImg = img;
        
        // 点击背景关闭
        modal.addEventListener('click', (e) => {
            if (e.target === modal) closeModal();
        });
        
        // 鼠标滚轮缩放
        modal.addEventListener('wheel', (e) => {
            e.preventDefault();
            if (e.deltaY < 0) zoomIn();
            else zoomOut();
        });
        
        // 键盘控制
        document.addEventListener('keydown', (e) => {
            if (modal.style.display === 'flex') {
                if (e.key === 'Escape') closeModal();
                else if (e.key === '+' || e.key === '=') zoomIn();
                else if (e.key === '-') zoomOut();
            }
        });
    }
    
    window.zoomIn = () => {
        scale = Math.min(scale * 1.2, 5);
        currentImg.style.transform = `scale(${scale})`;
    };
    
    window.zoomOut = () => {
        scale = Math.max(scale / 1.2, 0.5);
        currentImg.style.transform = `scale(${scale})`;
    };
    
    window.closeModal = () => {
        modal.style.display = 'none';
        scale = 1;
        currentImg.style.transform = 'scale(1)';
    };
    
    function openModal(imgSrc) {
        if (!modal) createModal();
        currentImg.src = imgSrc;
        modal.style.display = 'flex';
        scale = 1;
        currentImg.style.transform = 'scale(1)';
    }
    
    // 为所有图片添加点击事件
    function addClickToImages() {
        document.querySelectorAll('img').forEach(img => {
            img.style.cursor = 'zoom-in';
            img.addEventListener('click', () => openModal(img.src));
        });
    }
    
    // 页面加载完成后初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', addClickToImages);
    } else {
        addClickToImages();
    }
    
    // 监听动态添加的图片
    const observer = new MutationObserver(() => addClickToImages());
    observer.observe(document.body, { childList: true, subtree: true });
})();
