package com.example.providers

import com.example.models.NewsItem
import org.jsoup.Jsoup
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class GoogleNewsProvider : NewsProvider {
    override val name: String = "Google"

    override suspend fun search(keyword: String): List<NewsItem> = withContext(Dispatchers.IO) {
        try {
            val encodedKeyword = java.net.URLEncoder.encode(keyword, "UTF-8")
            val url = "https://news.google.com/rss/search?q=$encodedKeyword&hl=ko&gl=KR&ceid=KR:ko"
            
            val doc = Jsoup.connect(url)
                .timeout(3000) // 3초 타임아웃 설정
                .get()
            val items = doc.select("item")
            
            println("Google News: Found ${items.size} items for '$keyword'")

            items.map { item ->
                NewsItem(
                    title = item.select("title").text(),
                    link = item.select("link").text(),
                    summary = "발행일: ${item.select("pubDate").text()}",
                    source = name
                )
            }.take(10)
        } catch (e: Exception) {
            println("Google News Error: ${e.message}")
            emptyList()
        }
    }
}
