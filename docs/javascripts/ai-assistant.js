/**
 * AI Assistant Module
 * AI助手主模块 - 负责UI和核心交互
 */

(function() {
    'use strict';
    
    var assistant = {
        container: null,
        button: null,
        panel: null,
        chatHistory: null,
        inputBox: null,
        sendButton: null,
        configButton: null,
        configPanel: null,
        isOpen: false,
        messages: [],
        isProcessing: false,
        initialized: false
    };
    
    /**
     * 初始化AI助手
     */
    function initAssistant() {
        if (assistant.initialized) return;
        
        console.log('[AI Assistant] 初始化AI助手...');
        
        // 加载配置
        loadConfiguration();
        
        // 创建UI元素
        createFloatingButton();
        createChatPanel();
        createConfigPanel();
        
        // 加载历史对话
        loadChatHistory();
        
        // 键盘快捷键
        setupKeyboardShortcuts();
        
        assistant.initialized = true;
        console.log('[AI Assistant] AI助手初始化完成');
    }
    
    /**
     * 创建浮动按钮
     */
    function createFloatingButton() {
        var button = document.createElement('button');
        button.className = 'ai-assistant-button';
        button.innerHTML = '🤖<span class="tooltip">AI助手 (Ctrl+K)</span>';
        button.onclick = togglePanel;
        
        document.body.appendChild(button);
        assistant.button = button;
    }
    
    /**
     * 创建聊天面板
     */
    function createChatPanel() {
        var panel = document.createElement('div');
        panel.className = 'ai-assistant-panel';
        panel.style.display = 'none';
        
        // 头部
        var header = document.createElement('div');
        header.className = 'ai-panel-header';
        header.innerHTML = '<h3>🤖 AI护肤助手</h3>' +
            '<div class="header-actions">' +
            '<button class="config-btn" title="配置">⚙️</button>' +
            '<button class="clear-btn" title="清除对话">🗑️</button>' +
            '<button class="close-btn" title="关闭">✕</button>' +
            '</div>';
        
        // 聊天历史区域
        var chatHistory = document.createElement('div');
        chatHistory.className = 'ai-chat-history';
        
        // 输入区域
        var inputArea = document.createElement('div');
        inputArea.className = 'ai-input-area';
        
        var inputBox = document.createElement('textarea');
        inputBox.className = 'ai-input-box';
        inputBox.placeholder = '请输入您的问题...';
        inputBox.rows = 3;
        
        var sendButton = document.createElement('button');
        sendButton.className = 'ai-send-btn';
        sendButton.innerHTML = '发送';
        sendButton.onclick = handleSendMessage;
        
        inputArea.appendChild(inputBox);
        inputArea.appendChild(sendButton);
        
        // 组装面板
        panel.appendChild(header);
        panel.appendChild(chatHistory);
        panel.appendChild(inputArea);
        
        document.body.appendChild(panel);
        
        // 保存引用
        assistant.panel = panel;
        assistant.chatHistory = chatHistory;
        assistant.inputBox = inputBox;
        assistant.sendButton = sendButton;
        
        // 绑定事件
        header.querySelector('.config-btn').onclick = showConfigPanel;
        header.querySelector('.clear-btn').onclick = clearChatHistory;
        header.querySelector('.close-btn').onclick = hidePanel;
        
        // 输入框回车发送
        inputBox.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSendMessage();
            }
        });
    }
    
    /**
     * 创建配置面板
     */
    function createConfigPanel() {
        var panel = document.createElement('div');
        panel.className = 'ai-config-panel';
        panel.style.display = 'none';
        
        var config = window.AIConfig ? window.AIConfig.load() : {};
        var models = window.AIConfig ? window.AIConfig.getAllModels() : {};
        
        var html = '<div class="config-header">' +
            '<h3>⚙️ AI助手配置</h3>' +
            '<button class="close-btn">✕</button>' +
            '</div>' +
            '<div class="config-content">' +
            '<div class="config-section">' +
            '<label>选择大模型</label>' +
            '<select id="ai-model-type" class="config-input">';
        
        for (var key in models) {
            if (models.hasOwnProperty(key)) {
                var selected = config.modelType === key ? ' selected' : '';
                html += '<option value="' + key + '"' + selected + '>' + models[key].name + '</option>';
            }
        }
        
        html += '</select>' +
            '</div>' +
            '<div class="config-section">' +
            '<label>具体模型</label>' +
            '<select id="ai-model" class="config-input"></select>' +
            '</div>' +
            '<div class="config-section">' +
            '<label>API Key</label>' +
            '<input type="password" id="ai-api-key" class="config-input" placeholder="请输入API Key" value="' + (config.apiKey || '') + '">' +
            '</div>' +
            '<div class="config-section" id="secret-key-section" style="display:none">' +
            '<label>Secret Key (文心一言)</label>' +
            '<input type="password" id="ai-secret-key" class="config-input" placeholder="请输入Secret Key" value="' + (config.secretKey || '') + '">' +
            '</div>' +
            '<div class="config-section">' +
            '<label>API服务地址</label>' +
            '<input type="text" id="ai-api-url" class="config-input" value="' + (config.apiBaseUrl || 'http://localhost:8001') + '">' +
            '</div>' +
            '<div class="config-section">' +
            '<label>温度 (Temperature)</label>' +
            '<input type="range" id="ai-temperature" class="config-slider" min="0" max="1" step="0.1" value="' + (config.temperature || 0.7) + '">' +
            '<span class="slider-value">' + (config.temperature || 0.7) + '</span>' +
            '</div>' +
            '<div class="config-section">' +
            '<label>Top-P</label>' +
            '<input type="range" id="ai-top-p" class="config-slider" min="0" max="1" step="0.1" value="' + (config.topP || 0.9) + '">' +
            '<span class="slider-value">' + (config.topP || 0.9) + '</span>' +
            '</div>' +
            '<div class="config-section">' +
            '<label>最大回复长度 (Max Tokens)</label>' +
            '<input type="number" id="ai-max-tokens" class="config-input" min="100" max="4000" value="' + (config.maxTokens || 2000) + '">' +
            '</div>' +
            '<div class="config-section">' +
            '<label>系统提示词</label>' +
            '<textarea id="ai-system-prompt" class="config-textarea" rows="3">' + (config.systemPrompt || '') + '</textarea>' +
            '</div>' +
            '<div class="config-section">' +
            '<label><input type="checkbox" id="ai-use-rag" ' + (config.useRAG !== false ? 'checked' : '') + '> 启用知识库增强 (RAG)</label>' +
            '</div>' +
            '<div class="config-section">' +
            '<label><input type="checkbox" id="ai-stream" ' + (config.streamResponse !== false ? 'checked' : '') + '> 启用流式响应</label>' +
            '</div>' +
            '<div class="config-section">' +
            '<label><input type="checkbox" id="ai-local-storage" ' + (config.useLocalStorage !== false ? 'checked' : '') + '> 使用本地存储</label>' +
            '</div>' +
            '<div class="config-actions">' +
            '<button class="btn-test" id="test-connection-btn">测试连接</button>' +
            '<button class="btn-save" id="save-config-btn">保存配置</button>' +
            '<button class="btn-reset" id="reset-config-btn">重置</button>' +
            '</div>' +
            '<div class="config-status" id="config-status"></div>' +
            '</div>';
        
        panel.innerHTML = html;
        document.body.appendChild(panel);
        assistant.configPanel = panel;
        
        // 绑定事件
        panel.querySelector('.close-btn').onclick = hideConfigPanel;
        panel.querySelector('#save-config-btn').onclick = saveConfiguration;
        panel.querySelector('#reset-config-btn').onclick = resetConfiguration;
        panel.querySelector('#test-connection-btn').onclick = testConnection;
        
        var modelTypeSelect = panel.querySelector('#ai-model-type');
        modelTypeSelect.onchange = function() {
            updateModelOptions();
            updateSecretKeyVisibility();
        };
        
        // 滑块值实时更新
        var sliders = panel.querySelectorAll('.config-slider');
        for (var i = 0; i < sliders.length; i++) {
            sliders[i].oninput = function() {
                this.nextElementSibling.textContent = this.value;
            };
        }
        
        // 初始化模型选项
        updateModelOptions();
        updateSecretKeyVisibility();
    }
    
    /**
     * 更新模型选项
     */
    function updateModelOptions() {
        var modelTypeSelect = assistant.configPanel.querySelector('#ai-model-type');
        var modelSelect = assistant.configPanel.querySelector('#ai-model');
        var selectedType = modelTypeSelect.value;
        
        var models = window.AIConfig ? window.AIConfig.getAllModels() : {};
        var modelInfo = models[selectedType];
        
        if (!modelInfo) return;
        
        modelSelect.innerHTML = '';
        var modelList = modelInfo.models;
        for (var i = 0; i < modelList.length; i++) {
            var option = document.createElement('option');
            option.value = modelList[i].value;
            option.textContent = modelList[i].label;
            modelSelect.appendChild(option);
        }
    }
    
    /**
     * 更新Secret Key字段可见性
     */
    function updateSecretKeyVisibility() {
        var modelTypeSelect = assistant.configPanel.querySelector('#ai-model-type');
        var secretKeySection = assistant.configPanel.querySelector('#secret-key-section');
        var selectedType = modelTypeSelect.value;
        
        var models = window.AIConfig ? window.AIConfig.getAllModels() : {};
        var modelInfo = models[selectedType];
        
        if (modelInfo && modelInfo.needsSecretKey) {
            secretKeySection.style.display = 'block';
        } else {
            secretKeySection.style.display = 'none';
        }
    }
    
    /**
     * 切换面板显示
     */
    function togglePanel() {
        if (assistant.isOpen) {
            hidePanel();
        } else {
            showPanel();
        }
    }
    
    /**
     * 显示面板
     */
    function showPanel() {
        if (!assistant.panel) return;
        
        assistant.panel.style.display = 'block';
        setTimeout(function() {
            assistant.panel.classList.add('visible');
        }, 10);
        
        assistant.isOpen = true;
        assistant.inputBox.focus();
    }
    
    /**
     * 隐藏面板
     */
    function hidePanel() {
        if (!assistant.panel) return;
        
        assistant.panel.classList.remove('visible');
        setTimeout(function() {
            assistant.panel.style.display = 'none';
        }, 300);
        
        assistant.isOpen = false;
    }
    
    /**
     * 显示配置面板
     */
    function showConfigPanel() {
        if (!assistant.configPanel) return;
        assistant.configPanel.style.display = 'block';
    }
    
    /**
     * 隐藏配置面板
     */
    function hideConfigPanel() {
        if (!assistant.configPanel) return;
        assistant.configPanel.style.display = 'none';
    }
    
    /**
     * 加载配置
     */
    function loadConfiguration() {
        // 配置通过AIConfig模块管理
        console.log('[AI Assistant] 配置已加载');
    }
    
    /**
     * 保存配置
     */
    function saveConfiguration() {
        var panel = assistant.configPanel;
        var status = panel.querySelector('#config-status');
        
        var config = {
            modelType: panel.querySelector('#ai-model-type').value,
            model: panel.querySelector('#ai-model').value,
            apiKey: panel.querySelector('#ai-api-key').value,
            secretKey: panel.querySelector('#ai-secret-key').value,
            apiBaseUrl: panel.querySelector('#ai-api-url').value,
            temperature: parseFloat(panel.querySelector('#ai-temperature').value),
            topP: parseFloat(panel.querySelector('#ai-top-p').value),
            maxTokens: parseInt(panel.querySelector('#ai-max-tokens').value),
            systemPrompt: panel.querySelector('#ai-system-prompt').value,
            useRAG: panel.querySelector('#ai-use-rag').checked,
            streamResponse: panel.querySelector('#ai-stream').checked,
            useLocalStorage: panel.querySelector('#ai-local-storage').checked
        };
        
        if (window.AIConfig) {
            var validation = window.AIConfig.validate(config);
            if (!validation.valid) {
                status.textContent = '❌ ' + validation.errors.join('; ');
                status.className = 'config-status error';
                return;
            }
            
            if (window.AIConfig.save(config)) {
                status.textContent = '✅ 配置保存成功';
                status.className = 'config-status success';
                setTimeout(function() {
                    status.textContent = '';
                }, 3000);
            } else {
                status.textContent = '❌ 保存失败';
                status.className = 'config-status error';
            }
        }
    }
    
    /**
     * 重置配置
     */
    function resetConfiguration() {
        if (window.AIConfig && confirm('确定要重置所有配置吗？')) {
            window.AIConfig.reset();
            location.reload();
        }
    }
    
    /**
     * 测试连接
     */
    function testConnection() {
        var panel = assistant.configPanel;
        var status = panel.querySelector('#config-status');
        var button = panel.querySelector('#test-connection-btn');
        
        status.textContent = '🔄 测试中...';
        status.className = 'config-status';
        button.disabled = true;
        
        var config = {
            modelType: panel.querySelector('#ai-model-type').value,
            model: panel.querySelector('#ai-model').value,
            apiKey: panel.querySelector('#ai-api-key').value,
            secretKey: panel.querySelector('#ai-secret-key').value,
            apiBaseUrl: panel.querySelector('#ai-api-url').value
        };
        
        if (window.AIConfig) {
            window.AIConfig.testConnection(config, function(error, result) {
                button.disabled = false;
                if (error) {
                    status.textContent = '❌ 连接失败: ' + error.message;
                    status.className = 'config-status error';
                } else {
                    status.textContent = '✅ 连接成功! 模型: ' + result.model;
                    status.className = 'config-status success';
                }
            });
        }
    }
    
    /**
     * 处理发送消息
     */
    function handleSendMessage() {
        var message = assistant.inputBox.value.trim();
        if (!message || assistant.isProcessing) return;
        
        sendMessage(message);
        assistant.inputBox.value = '';
    }
    
    /**
     * 发送消息
     */
    function sendMessage(message) {
        if (!window.AIConfig) {
            addSystemMessage('错误：配置模块未加载');
            return;
        }
        
        var config = window.AIConfig.load();
        
        if (!config.apiKey) {
            addSystemMessage('请先配置API Key');
            showConfigPanel();
            return;
        }
        
        // 添加用户消息到界面
        addUserMessage(message);
        
        // 构建消息列表
        var messages = buildMessageList(message, config);
        
        // 显示加载状态
        var loadingId = addLoadingMessage();
        assistant.isProcessing = true;
        
        // 调用API
        if (config.streamResponse) {
            callStreamAPI(messages, config, loadingId);
        } else {
            callAPI(messages, config, loadingId);
        }
    }
    
    /**
     * 构建消息列表
     */
    function buildMessageList(userMessage, config) {
        var messages = [];
        
        // 添加系统提示
        if (config.systemPrompt) {
            var systemPrompt = config.systemPrompt;
            
            // 如果启用RAG，增强提示词
            if (config.useRAG && window.AIKnowledge) {
                systemPrompt = window.AIKnowledge.buildEnhancedPrompt(userMessage, config.systemPrompt);
            }
            
            messages.push({
                role: 'system',
                content: systemPrompt
            });
        }
        
        // 添加历史对话（最近5轮）
        var recentMessages = assistant.messages.slice(-10); // 5轮对话=10条消息
        for (var i = 0; i < recentMessages.length; i++) {
            messages.push(recentMessages[i]);
        }
        
        // 添加当前用户消息
        messages.push({
            role: 'user',
            content: userMessage
        });
        
        return messages;
    }
    
    /**
     * 调用API（非流式）
     */
    function callAPI(messages, config, loadingId) {
        var apiUrl = config.apiBaseUrl + '/api/chat';
        
        var requestData = {
            model_type: config.modelType,
            api_key: config.apiKey,
            messages: messages,
            config: {
                model: config.model,
                temperature: config.temperature,
                top_p: config.topP,
                max_tokens: config.maxTokens,
                secret_key: config.secretKey
            },
            stream: false
        };
        
        fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        })
        .then(function(response) {
            if (!response.ok) {
                return response.json().then(function(error) {
                    throw new Error(error.detail || '请求失败');
                });
            }
            return response.json();
        })
        .then(function(data) {
            removeMessage(loadingId);
            addAssistantMessage(data.content);
            assistant.isProcessing = false;
            
            // 保存到历史
            saveMessageToHistory('user', messages[messages.length - 1].content);
            saveMessageToHistory('assistant', data.content);
        })
        .catch(function(error) {
            removeMessage(loadingId);
            addSystemMessage('错误: ' + error.message);
            assistant.isProcessing = false;
        });
    }
    
    /**
     * 调用API（流式）
     */
    function callStreamAPI(messages, config, loadingId) {
        var apiUrl = config.apiBaseUrl + '/api/chat';
        
        var requestData = {
            model_type: config.modelType,
            api_key: config.apiKey,
            messages: messages,
            config: {
                model: config.model,
                temperature: config.temperature,
                top_p: config.topP,
                max_tokens: config.maxTokens,
                secret_key: config.secretKey
            },
            stream: true
        };
        
        fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        })
        .then(function(response) {
            if (!response.ok) {
                throw new Error('请求失败: ' + response.statusText);
            }
            
            removeMessage(loadingId);
            var messageId = addAssistantMessage('');
            var fullContent = '';
            
            var reader = response.body.getReader();
            var decoder = new TextDecoder();
            
            function readStream() {
                reader.read().then(function(result) {
                    if (result.done) {
                        assistant.isProcessing = false;
                        // 保存到历史
                        saveMessageToHistory('user', messages[messages.length - 1].content);
                        saveMessageToHistory('assistant', fullContent);
                        return;
                    }
                    
                    var chunk = decoder.decode(result.value, { stream: true });
                    var lines = chunk.split('\n');
                    
                    for (var i = 0; i < lines.length; i++) {
                        var line = lines[i].trim();
                        if (line.startsWith('data: ')) {
                            var data = line.substring(6);
                            if (data && data !== '[DONE]' && !data.startsWith('[ERROR')) {
                                fullContent += data;
                                updateMessage(messageId, fullContent);
                            } else if (data.startsWith('[ERROR')) {
                                addSystemMessage('错误: ' + data);
                            }
                        }
                    }
                    
                    readStream();
                }).catch(function(error) {
                    assistant.isProcessing = false;
                    addSystemMessage('流式读取错误: ' + error.message);
                });
            }
            
            readStream();
        })
        .catch(function(error) {
            removeMessage(loadingId);
            addSystemMessage('错误: ' + error.message);
            assistant.isProcessing = false;
        });
    }
    
    /**
     * 添加用户消息
     */
    function addUserMessage(content) {
        return addMessage('user', content);
    }
    
    /**
     * 添加AI消息
     */
    function addAssistantMessage(content) {
        return addMessage('assistant', content);
    }
    
    /**
     * 添加系统消息
     */
    function addSystemMessage(content) {
        return addMessage('system', content);
    }
    
    /**
     * 添加加载消息
     */
    function addLoadingMessage() {
        return addMessage('loading', '思考中...');
    }
    
    /**
     * 添加消息
     */
    function addMessage(role, content) {
        var messageId = 'msg-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9);
        
        var messageDiv = document.createElement('div');
        messageDiv.className = 'ai-message ai-message-' + role;
        messageDiv.id = messageId;
        
        if (role === 'loading') {
            messageDiv.innerHTML = '<div class="message-content loading-dots">' + content + '</div>';
        } else {
            var icon = role === 'user' ? '👤' : (role === 'assistant' ? '🤖' : 'ℹ️');
            messageDiv.innerHTML = '<div class="message-icon">' + icon + '</div>' +
                '<div class="message-content">' + escapeHtml(content) + '</div>';
        }
        
        assistant.chatHistory.appendChild(messageDiv);
        assistant.chatHistory.scrollTop = assistant.chatHistory.scrollHeight;
        
        return messageId;
    }
    
    /**
     * 更新消息
     */
    function updateMessage(messageId, content) {
        var messageDiv = document.getElementById(messageId);
        if (messageDiv) {
            var contentDiv = messageDiv.querySelector('.message-content');
            if (contentDiv) {
                contentDiv.textContent = content;
            }
            assistant.chatHistory.scrollTop = assistant.chatHistory.scrollHeight;
        }
    }
    
    /**
     * 删除消息
     */
    function removeMessage(messageId) {
        var messageDiv = document.getElementById(messageId);
        if (messageDiv) {
            messageDiv.remove();
        }
    }
    
    /**
     * 保存消息到历史
     */
    function saveMessageToHistory(role, content) {
        assistant.messages.push({
            role: role,
            content: content,
            timestamp: Date.now()
        });
        
        // 限制历史消息数量
        if (assistant.messages.length > 50) {
            assistant.messages = assistant.messages.slice(-50);
        }
        
        // 保存到localStorage
        try {
            localStorage.setItem('ai_chat_history', JSON.stringify(assistant.messages));
        } catch (e) {
            console.warn('[AI Assistant] 无法保存对话历史:', e);
        }
    }
    
    /**
     * 加载对话历史
     */
    function loadChatHistory() {
        try {
            var stored = localStorage.getItem('ai_chat_history');
            if (stored) {
                assistant.messages = JSON.parse(stored);
                
                // 显示最近的对话
                var recentMessages = assistant.messages.slice(-10);
                for (var i = 0; i < recentMessages.length; i++) {
                    var msg = recentMessages[i];
                    if (msg.role === 'user') {
                        addUserMessage(msg.content);
                    } else if (msg.role === 'assistant') {
                        addAssistantMessage(msg.content);
                    }
                }
            }
        } catch (e) {
            console.warn('[AI Assistant] 无法加载对话历史:', e);
        }
    }
    
    /**
     * 清除对话历史
     */
    function clearChatHistory() {
        if (!confirm('确定要清除所有对话历史吗？')) return;
        
        assistant.messages = [];
        assistant.chatHistory.innerHTML = '';
        
        try {
            localStorage.removeItem('ai_chat_history');
        } catch (e) {
            console.warn('[AI Assistant] 无法清除对话历史:', e);
        }
    }
    
    /**
     * 设置键盘快捷键
     */
    function setupKeyboardShortcuts() {
        document.addEventListener('keydown', function(e) {
            // Ctrl/Cmd + K 呼出助手
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                togglePanel();
            }
        });
    }
    
    /**
     * HTML转义
     */
    function escapeHtml(text) {
        var div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    // 页面加载时初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initAssistant);
    } else {
        initAssistant();
    }
    
    // 导出API
    window.AIAssistant = {
        show: showPanel,
        hide: hidePanel,
        sendMessage: sendMessage,
        clearHistory: clearChatHistory
    };
    
})();
