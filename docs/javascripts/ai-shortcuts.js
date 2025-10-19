/**
 * AI Shortcuts Module
 * AI助手快捷功能模块
 */

(function() {
    'use strict';
    
    var shortcuts = {
        selectionMenu: null,
        selectedText: '',
        initialized: false
    };
    
    // 快捷操作配置
    var shortcutActions = {
        explain: {
            icon: '💡',
            label: '解释这段内容',
            prompt: '请解释以下内容的含义：\n\n'
        },
        analyze: {
            icon: '🔍',
            label: '深入分析',
            prompt: '请深入分析以下内容，包括其原理、应用和注意事项：\n\n'
        },
        expand: {
            icon: '📚',
            label: '相关知识拓展',
            prompt: '请围绕以下内容，拓展相关的护肤知识：\n\n'
        },
        notes: {
            icon: '📝',
            label: '生成学习笔记',
            prompt: '请将以下内容整理成学习笔记，包括要点总结：\n\n'
        }
    };
    
    // 预设快捷按钮
    var presetActions = [
        {
            icon: '📋',
            label: '总结本章',
            prompt: '请总结当前章节的主要内容和要点。'
        },
        {
            icon: '❓',
            label: '生成知识测验',
            prompt: '基于当前章节内容，生成3-5个测验问题，帮助我检验学习效果。'
        },
        {
            icon: '🔗',
            label: '推荐相关内容',
            prompt: '基于当前内容，推荐相关的护肤知识或章节供进一步学习。'
        },
        {
            icon: '💬',
            label: '问题解答',
            prompt: '我对当前内容有疑问，希望得到详细解答。'
        }
    ];
    
    /**
     * 初始化快捷功能
     */
    function initShortcuts() {
        if (shortcuts.initialized) return;
        
        console.log('[AI Shortcuts] 初始化快捷功能...');
        
        // 创建选择菜单
        createSelectionMenu();
        
        // 监听文本选择
        document.addEventListener('mouseup', handleTextSelection);
        document.addEventListener('touchend', handleTextSelection);
        
        // 监听点击外部关闭菜单
        document.addEventListener('click', function(e) {
            if (shortcuts.selectionMenu && 
                !shortcuts.selectionMenu.contains(e.target)) {
                hideSelectionMenu();
            }
        });
        
        shortcuts.initialized = true;
        console.log('[AI Shortcuts] 快捷功能初始化完成');
    }
    
    /**
     * 创建选择菜单
     */
    function createSelectionMenu() {
        var menu = document.createElement('div');
        menu.className = 'ai-selection-menu';
        menu.style.display = 'none';
        
        // 添加快捷操作按钮
        for (var key in shortcutActions) {
            if (shortcutActions.hasOwnProperty(key)) {
                var action = shortcutActions[key];
                var button = createMenuButton(action.icon, action.label, function(act) {
                    return function() {
                        handleShortcutAction(act);
                    };
                }(action));
                menu.appendChild(button);
            }
        }
        
        document.body.appendChild(menu);
        shortcuts.selectionMenu = menu;
    }
    
    /**
     * 创建菜单按钮
     */
    function createMenuButton(icon, label, onClick) {
        var button = document.createElement('button');
        button.className = 'ai-shortcut-btn';
        button.innerHTML = '<span class="icon">' + icon + '</span><span class="label">' + label + '</span>';
        button.onclick = onClick;
        return button;
    }
    
    /**
     * 处理文本选择
     */
    function handleTextSelection(e) {
        var selection = window.getSelection();
        var selectedText = selection.toString().trim();
        
        if (selectedText && selectedText.length > 5 && selectedText.length < 1000) {
            shortcuts.selectedText = selectedText;
            showSelectionMenu(e);
        } else {
            hideSelectionMenu();
        }
    }
    
    /**
     * 显示选择菜单
     */
    function showSelectionMenu(e) {
        if (!shortcuts.selectionMenu) return;
        
        var menu = shortcuts.selectionMenu;
        var x = e.pageX || (e.changedTouches && e.changedTouches[0].pageX);
        var y = e.pageY || (e.changedTouches && e.changedTouches[0].pageY);
        
        // 计算位置，避免超出视口
        var menuWidth = 250;
        var menuHeight = 200;
        var viewportWidth = window.innerWidth;
        var viewportHeight = window.innerHeight;
        
        var left = x + 10;
        var top = y + 10;
        
        if (left + menuWidth > viewportWidth) {
            left = x - menuWidth - 10;
        }
        
        if (top + menuHeight > viewportHeight + window.scrollY) {
            top = y - menuHeight - 10;
        }
        
        menu.style.left = left + 'px';
        menu.style.top = top + 'px';
        menu.style.display = 'block';
        
        // 添加动画
        setTimeout(function() {
            menu.classList.add('visible');
        }, 10);
    }
    
    /**
     * 隐藏选择菜单
     */
    function hideSelectionMenu() {
        if (!shortcuts.selectionMenu) return;
        
        var menu = shortcuts.selectionMenu;
        menu.classList.remove('visible');
        setTimeout(function() {
            menu.style.display = 'none';
        }, 200);
    }
    
    /**
     * 处理快捷操作
     */
    function handleShortcutAction(action) {
        hideSelectionMenu();
        
        var prompt = action.prompt + shortcuts.selectedText;
        
        // 触发AI助手发送消息
        if (window.AIAssistant && window.AIAssistant.sendMessage) {
            window.AIAssistant.show();
            window.AIAssistant.sendMessage(prompt);
        } else {
            console.warn('[AI Shortcuts] AI助手未就绪');
        }
    }
    
    /**
     * 创建预设快捷按钮面板
     */
    function createPresetPanel() {
        // 检查是否已存在
        if (document.querySelector('.ai-preset-panel')) return;
        
        var panel = document.createElement('div');
        panel.className = 'ai-preset-panel';
        
        var title = document.createElement('div');
        title.className = 'panel-title';
        title.textContent = 'AI快捷功能';
        panel.appendChild(title);
        
        var buttonsContainer = document.createElement('div');
        buttonsContainer.className = 'preset-buttons';
        
        for (var i = 0; i < presetActions.length; i++) {
            var action = presetActions[i];
            var button = createPresetButton(action);
            buttonsContainer.appendChild(button);
        }
        
        panel.appendChild(buttonsContainer);
        
        // 添加到页面（可以选择合适的位置）
        var content = document.querySelector('.md-content');
        if (content) {
            content.appendChild(panel);
        }
    }
    
    /**
     * 创建预设按钮
     */
    function createPresetButton(action) {
        var button = document.createElement('button');
        button.className = 'ai-preset-btn';
        button.innerHTML = action.icon + ' ' + action.label;
        button.onclick = function() {
            if (window.AIAssistant && window.AIAssistant.sendMessage) {
                window.AIAssistant.show();
                
                // 如果使用RAG，构建增强提示
                var prompt = action.prompt;
                if (window.AIKnowledge && window.AIConfig) {
                    var config = window.AIConfig.load();
                    if (config.useRAG) {
                        prompt = window.AIKnowledge.buildEnhancedPrompt(action.prompt, '');
                        // 将原始问题添加到末尾
                        prompt = prompt + '\n\n用户问题：' + action.prompt;
                    }
                }
                
                window.AIAssistant.sendMessage(action.prompt);
            }
        };
        return button;
    }
    
    /**
     * 获取快捷操作列表
     */
    function getShortcutActions() {
        return shortcutActions;
    }
    
    /**
     * 获取预设操作列表
     */
    function getPresetActions() {
        return presetActions;
    }
    
    /**
     * 添加自定义快捷操作
     */
    function addCustomAction(key, action) {
        if (!action.icon || !action.label || !action.prompt) {
            console.error('[AI Shortcuts] 无效的快捷操作配置');
            return false;
        }
        
        shortcutActions[key] = action;
        
        // 重新创建选择菜单
        if (shortcuts.selectionMenu) {
            shortcuts.selectionMenu.remove();
            shortcuts.selectionMenu = null;
            createSelectionMenu();
        }
        
        return true;
    }
    
    // 页面加载时初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            initShortcuts();
            // 可选：创建预设按钮面板
            // createPresetPanel();
        });
    } else {
        initShortcuts();
        // createPresetPanel();
    }
    
    // 导出API
    window.AIShortcuts = {
        init: initShortcuts,
        getActions: getShortcutActions,
        getPresets: getPresetActions,
        addAction: addCustomAction,
        createPresetPanel: createPresetPanel
    };
    
})();
