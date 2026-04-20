package com.example.services

import com.example.models.NewsItem
import com.example.providers.NewsProvider

class NewsService(private val providers: List<NewsProvider>) {
    suspend fun getNews(keyword: String, source: String? = null): List<NewsItem> {
        val selectedProviders = if (source == null) {
            providers
        } else {
            providers.filter { it.name.equals(source, ignoreCase = true) }
        }

        return selectedProviders.flatMap { it.search(keyword) }
    }
}
