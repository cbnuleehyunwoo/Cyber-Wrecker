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
            // 구글 뉴스는 RSS를 제공하므로 크롤링 차단이 없으며 매우 정확합니다.
            val url = "https://news.google.com/rss/search?q=$encodedKeyword&hl=ko&gl=KR&ceid=KR:ko"
            
            val doc = Jsoup.connect(url).get()
            val items = doc.select("item")

            items.map { item ->
                NewsItem(
                    title = item.select("title").text(),
                    link = item.select("link").text(),
                    summary = "발행일: ${item.select("pubDate").text()}",
                    source = name
                )
            }.take(10) // 상위 10개만
        } catch (e: Exception) {
            println("Google News Error: ${e.message}")
            emptyList()
        }
    }
}
