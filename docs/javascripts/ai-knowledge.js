/**
 * AI Knowledge Base Module
 * 本地知识库模块 - 提取和检索电子书内容
 */

(function() {
    'use strict';
    
    // 知识库存储
    var knowledgeBase = {
        chapters: [],
        index: {},
        initialized: false
    };
    
    /**
     * 初始化知识库
     */
    function initKnowledgeBase() {
        if (knowledgeBase.initialized) return;
        
        console.log('[AI Knowledge] 初始化知识库...');
        extractBookContent();
        buildIndex();
        knowledgeBase.initialized = true;
        console.log('[AI Knowledge] 知识库初始化完成，共 ' + knowledgeBase.chapters.length + ' 个章节');
    }
    
    /**
     * 提取电子书内容
     */
    function extractBookContent() {
        var mainContent = document.querySelector('.md-content');
        if (!mainContent) return;
        
        // 获取当前页面标题和内容
        var titleElement = mainContent.querySelector('h1');
        var title = titleElement ? titleElement.textContent : '未知章节';
        
        // 提取所有段落文本
        var paragraphs = mainContent.querySelectorAll('p, li, blockquote');
        var content = [];
        
        for (var i = 0; i < paragraphs.length; i++) {
            var text = paragraphs[i].textContent.trim();
            if (text && text.length > 10) {
                content.push(text);
            }
        }
        
        // 提取标题结构
        var sections = [];
        var headers = mainContent.querySelectorAll('h2, h3, h4');
        for (var j = 0; j < headers.length; j++) {
            sections.push({
                level: headers[j].tagName,
                text: headers[j].textContent,
                id: headers[j].id || ''
            });
        }
        
        // 保存章节信息
        var chapter = {
            title: title,
            url: window.location.pathname,
            content: content.join('\n'),
            sections: sections,
            timestamp: new Date().getTime()
        };
        
        knowledgeBase.chapters.push(chapter);
        
        // 存储到localStorage（如果需要持久化）
        try {
            var stored = localStorage.getItem('ai_knowledge_base');
            var allChapters = stored ? JSON.parse(stored) : [];
            
            // 检查是否已存在该页面
            var exists = false;
            for (var k = 0; k < allChapters.length; k++) {
                if (allChapters[k].url === chapter.url) {
                    allChapters[k] = chapter;
                    exists = true;
                    break;
                }
            }
            
            if (!exists) {
                allChapters.push(chapter);
            }
            
            // 限制存储数量，避免超出localStorage限制
            if (allChapters.length > 50) {
                allChapters = allChapters.slice(-50);
            }
            
            localStorage.setItem('ai_knowledge_base', JSON.stringify(allChapters));
        } catch (e) {
            console.warn('[AI Knowledge] 无法存储到localStorage:', e);
        }
    }
    
    /**
     * 构建简单的关键词索引
     */
    function buildIndex() {
        knowledgeBase.index = {};
        
        for (var i = 0; i < knowledgeBase.chapters.length; i++) {
            var chapter = knowledgeBase.chapters[i];
            var words = extractKeywords(chapter.title + ' ' + chapter.content);
            
            for (var j = 0; j < words.length; j++) {
                var word = words[j];
                if (!knowledgeBase.index[word]) {
                    knowledgeBase.index[word] = [];
                }
                knowledgeBase.index[word].push(i);
            }
        }
    }
    
    /**
     * 提取关键词（简单分词）
     */
    function extractKeywords(text) {
        // 移除标点符号
        text = text.replace(/[，。！？；：、""''（）《》【】]/g, ' ');
        
        // 简单的中文分词（按字切分，2-4字词）
        var words = [];
        for (var i = 0; i < text.length - 1; i++) {
            // 2字词
            words.push(text.substr(i, 2));
            // 3字词
            if (i < text.length - 2) {
                words.push(text.substr(i, 3));
            }
            // 4字词
            if (i < text.length - 3) {
                words.push(text.substr(i, 4));
            }
        }
        
        return words;
    }
    
    /**
     * 搜索相关内容
     */
    function searchRelevantContent(query, limit) {
        limit = limit || 3;
        
        if (!knowledgeBase.initialized) {
            initKnowledgeBase();
        }
        
        // 提取查询关键词
        var keywords = extractKeywords(query);
        var scores = {};
        
        // 计算每个章节的相关度分数
        for (var i = 0; i < keywords.length; i++) {
            var word = keywords[i];
            var chapters = knowledgeBase.index[word] || [];
            
            for (var j = 0; j < chapters.length; j++) {
                var chapterIdx = chapters[j];
                scores[chapterIdx] = (scores[chapterIdx] || 0) + 1;
            }
        }
        
        // 排序并返回前N个相关章节
        var results = [];
        for (var idx in scores) {
            if (scores.hasOwnProperty(idx)) {
                results.push({
                    chapter: knowledgeBase.chapters[idx],
                    score: scores[idx]
                });
            }
        }
        
        results.sort(function(a, b) {
            return b.score - a.score;
        });
        
        return results.slice(0, limit);
    }
    
    /**
     * 获取上下文信息
     */
    function getContextInfo() {
        var mainContent = document.querySelector('.md-content');
        if (!mainContent) return null;
        
        var titleElement = mainContent.querySelector('h1');
        var title = titleElement ? titleElement.textContent : '';
        
        // 获取第一段作为摘要
        var firstParagraph = mainContent.querySelector('p');
        var summary = firstParagraph ? firstParagraph.textContent.substr(0, 200) : '';
        
        return {
            title: title,
            summary: summary,
            url: window.location.pathname
        };
    }
    
    /**
     * 构建增强的提示词（包含相关知识）
     */
    function buildEnhancedPrompt(userQuery, systemPrompt) {
        var context = getContextInfo();
        var relevantContent = searchRelevantContent(userQuery, 2);
        
        var enhancedPrompt = systemPrompt || '你是一个专业的护肤和刷酸知识助手。';
        
        // 添加当前页面上下文
        if (context) {
            enhancedPrompt += '\n\n【当前页面】\n' + 
                              '标题：' + context.title + '\n' +
                              '摘要：' + context.summary;
        }
        
        // 添加相关知识
        if (relevantContent.length > 0) {
            enhancedPrompt += '\n\n【相关知识】';
            for (var i = 0; i < relevantContent.length; i++) {
                var item = relevantContent[i];
                var excerpt = item.chapter.content.substr(0, 300);
                enhancedPrompt += '\n\n' + item.chapter.title + ':\n' + excerpt + '...';
            }
        }
        
        enhancedPrompt += '\n\n请基于以上内容回答用户的问题。';
        
        return enhancedPrompt;
    }
    
    /**
     * 加载存储的知识库
     */
    function loadStoredKnowledgeBase() {
        try {
            var stored = localStorage.getItem('ai_knowledge_base');
            if (stored) {
                var allChapters = JSON.parse(stored);
                knowledgeBase.chapters = allChapters;
                buildIndex();
                console.log('[AI Knowledge] 从存储加载了 ' + allChapters.length + ' 个章节');
            }
        } catch (e) {
            console.warn('[AI Knowledge] 无法加载存储的知识库:', e);
        }
    }
    
    // 页面加载时初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            loadStoredKnowledgeBase();
            initKnowledgeBase();
        });
    } else {
        loadStoredKnowledgeBase();
        initKnowledgeBase();
    }
    
    // 导出API
    window.AIKnowledge = {
        search: searchRelevantContent,
        getContext: getContextInfo,
        buildEnhancedPrompt: buildEnhancedPrompt,
        init: initKnowledgeBase
    };
    
})();
