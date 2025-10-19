/**
 * AI Config Module
 * AI助手配置管理模块
 */

(function() {
    'use strict';
    
    // 配置存储键
    var STORAGE_KEY = 'ai_assistant_config';
    var STORAGE_KEY_ENCRYPTED = 'ai_assistant_config_encrypted';
    
    // 默认配置
    var defaultConfig = {
        modelType: 'qwen',
        model: 'qwen-turbo',
        apiKey: '',
        secretKey: '', // 用于文心一言
        temperature: 0.7,
        topP: 0.9,
        maxTokens: 2000,
        systemPrompt: '你是一个专业的护肤和刷酸知识助手，擅长回答关于皮肤护理、刷酸方法、产品选择等问题。请用专业但易懂的语言回答，并在必要时提供安全提醒。',
        useRAG: true,
        streamResponse: true,
        useLocalStorage: true,
        apiBaseUrl: 'http://localhost:8001'
    };
    
    // 模型配置
    var modelConfigs = {
        qwen: {
            name: '通义千问',
            models: [
                { value: 'qwen-turbo', label: 'Qwen-Turbo (快速)' },
                { value: 'qwen-plus', label: 'Qwen-Plus (均衡)' },
                { value: 'qwen-max', label: 'Qwen-Max (旗舰)' }
            ],
            needsSecretKey: false,
            apiDoc: 'https://help.aliyun.com/zh/dashscope/'
        },
        ernie: {
            name: '文心一言',
            models: [
                { value: 'ernie-bot-turbo', label: 'ERNIE-Bot-turbo (快速)' },
                { value: 'ernie-bot', label: 'ERNIE-Bot (标准)' },
                { value: 'ernie-bot-4', label: 'ERNIE-Bot-4 (旗舰)' }
            ],
            needsSecretKey: true,
            apiDoc: 'https://cloud.baidu.com/doc/WENXINWORKSHOP/'
        },
        glm: {
            name: '智谱GLM',
            models: [
                { value: 'glm-4', label: 'GLM-4 (标准)' },
                { value: 'glm-4-flash', label: 'GLM-4-Flash (快速)' },
                { value: 'glm-3-turbo', label: 'GLM-3-Turbo' }
            ],
            needsSecretKey: false,
            apiDoc: 'https://open.bigmodel.cn/dev/api'
        },
        spark: {
            name: '讯飞星火',
            models: [
                { value: 'spark-lite', label: 'Spark-Lite (轻量)' },
                { value: 'spark-pro', label: 'Spark-Pro (专业)' },
                { value: 'spark-max', label: 'Spark-Max (旗舰)' }
            ],
            needsSecretKey: false,
            apiDoc: 'https://www.xfyun.cn/doc/spark/Web.html'
        },
        kimi: {
            name: 'Kimi',
            models: [
                { value: 'moonshot-v1-8k', label: 'Moonshot-v1-8k' },
                { value: 'moonshot-v1-32k', label: 'Moonshot-v1-32k' },
                { value: 'moonshot-v1-128k', label: 'Moonshot-v1-128k' }
            ],
            needsSecretKey: false,
            apiDoc: 'https://platform.moonshot.cn/docs'
        },
        doubao: {
            name: '豆包',
            models: [
                { value: 'doubao-lite-4k', label: 'Doubao-Lite-4k' },
                { value: 'doubao-pro-4k', label: 'Doubao-Pro-4k' },
                { value: 'doubao-pro-32k', label: 'Doubao-Pro-32k' }
            ],
            needsSecretKey: false,
            apiDoc: 'https://www.volcengine.com/docs/82379'
        }
    };
    
    // 简单加密/解密函数（Base64 + 简单混淆）
    function encryptKey(key) {
        if (!key) return '';
        var salt = 'ai_assistant_salt_2025';
        var mixed = '';
        for (var i = 0; i < key.length; i++) {
            var c = key.charCodeAt(i);
            var s = salt.charCodeAt(i % salt.length);
            mixed += String.fromCharCode(c ^ s);
        }
        return btoa(mixed);
    }
    
    function decryptKey(encrypted) {
        if (!encrypted) return '';
        try {
            var mixed = atob(encrypted);
            var salt = 'ai_assistant_salt_2025';
            var key = '';
            for (var i = 0; i < mixed.length; i++) {
                var c = mixed.charCodeAt(i);
                var s = salt.charCodeAt(i % salt.length);
                key += String.fromCharCode(c ^ s);
            }
            return key;
        } catch (e) {
            console.error('[AI Config] 解密失败:', e);
            return '';
        }
    }
    
    /**
     * 加载配置
     */
    function loadConfig() {
        try {
            var stored = localStorage.getItem(STORAGE_KEY);
            var storedEncrypted = localStorage.getItem(STORAGE_KEY_ENCRYPTED);
            
            if (!stored && !storedEncrypted) {
                return Object.assign({}, defaultConfig);
            }
            
            var config = stored ? JSON.parse(stored) : Object.assign({}, defaultConfig);
            
            // 解密敏感信息
            if (storedEncrypted) {
                var encrypted = JSON.parse(storedEncrypted);
                config.apiKey = decryptKey(encrypted.apiKey);
                config.secretKey = decryptKey(encrypted.secretKey);
            }
            
            // 合并默认配置（处理新增字段）
            return Object.assign({}, defaultConfig, config);
        } catch (e) {
            console.error('[AI Config] 加载配置失败:', e);
            return Object.assign({}, defaultConfig);
        }
    }
    
    /**
     * 保存配置
     */
    function saveConfig(config) {
        try {
            // 分离敏感信息
            var publicConfig = Object.assign({}, config);
            var encryptedConfig = {
                apiKey: encryptKey(config.apiKey),
                secretKey: encryptKey(config.secretKey)
            };
            
            // 从公开配置中移除敏感信息
            delete publicConfig.apiKey;
            delete publicConfig.secretKey;
            
            // 保存
            if (config.useLocalStorage) {
                localStorage.setItem(STORAGE_KEY, JSON.stringify(publicConfig));
                localStorage.setItem(STORAGE_KEY_ENCRYPTED, JSON.stringify(encryptedConfig));
            } else {
                // 使用sessionStorage
                sessionStorage.setItem(STORAGE_KEY, JSON.stringify(publicConfig));
                sessionStorage.setItem(STORAGE_KEY_ENCRYPTED, JSON.stringify(encryptedConfig));
            }
            
            return true;
        } catch (e) {
            console.error('[AI Config] 保存配置失败:', e);
            return false;
        }
    }
    
    /**
     * 重置配置
     */
    function resetConfig() {
        try {
            localStorage.removeItem(STORAGE_KEY);
            localStorage.removeItem(STORAGE_KEY_ENCRYPTED);
            sessionStorage.removeItem(STORAGE_KEY);
            sessionStorage.removeItem(STORAGE_KEY_ENCRYPTED);
            return true;
        } catch (e) {
            console.error('[AI Config] 重置配置失败:', e);
            return false;
        }
    }
    
    /**
     * 验证配置
     */
    function validateConfig(config) {
        var errors = [];
        
        if (!config.modelType) {
            errors.push('请选择模型类型');
        }
        
        if (!config.apiKey) {
            errors.push('请输入API Key');
        }
        
        if (config.modelType === 'ernie' && !config.secretKey) {
            errors.push('文心一言需要Secret Key');
        }
        
        if (config.temperature < 0 || config.temperature > 1) {
            errors.push('温度参数必须在0-1之间');
        }
        
        if (config.topP < 0 || config.topP > 1) {
            errors.push('Top-P参数必须在0-1之间');
        }
        
        if (config.maxTokens < 100 || config.maxTokens > 4000) {
            errors.push('最大Token数必须在100-4000之间');
        }
        
        return {
            valid: errors.length === 0,
            errors: errors
        };
    }
    
    /**
     * 获取当前模型配置信息
     */
    function getModelInfo(modelType) {
        return modelConfigs[modelType] || null;
    }
    
    /**
     * 获取所有模型配置
     */
    function getAllModels() {
        return modelConfigs;
    }
    
    /**
     * 测试连接
     */
    function testConnection(config, callback) {
        var apiUrl = config.apiBaseUrl + '/api/test-connection';
        
        var requestData = {
            model_type: config.modelType,
            api_key: config.apiKey,
            config: {
                model: config.model,
                secret_key: config.secretKey
            }
        };
        
        // 使用fetch API
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
                    throw new Error(error.detail || '连接失败');
                });
            }
            return response.json();
        })
        .then(function(data) {
            callback(null, data);
        })
        .catch(function(error) {
            callback(error, null);
        });
    }
    
    // 导出API
    window.AIConfig = {
        load: loadConfig,
        save: saveConfig,
        reset: resetConfig,
        validate: validateConfig,
        getModelInfo: getModelInfo,
        getAllModels: getAllModels,
        testConnection: testConnection,
        defaultConfig: defaultConfig
    };
    
})();
