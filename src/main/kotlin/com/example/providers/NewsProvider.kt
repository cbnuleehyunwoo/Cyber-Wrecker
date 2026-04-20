package com.example.providers

import com.example.models.NewsItem

interface NewsProvider {
    val name: String
    suspend fun search(keyword: String): List<NewsItem>
}
