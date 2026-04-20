package com.example.providers

import com.example.models.NewsItem
import org.jsoup.Jsoup
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class NaverNewsProvider : NewsProvider {
    override val name: String = "Naver"
override suspend fun search(keyword: String): List<NewsItem> = withContext(Dispatchers.IO) {
    try {
        val encodedKeyword = java.net.URLEncoder.encode(keyword, "UTF-8")
        // 상세 파라미터 추가 (nso, start 등)하여 실제 브라우저 요청처럼 위장
        val url = "https://search.naver.com/search.naver?where=news&query=$encodedKeyword&sm=tab_pge&sort=0&nso=so:r,p:all,a:all&start=1"

        val doc = Jsoup.connect(url)
            .userAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
            .header("Referer", "https://www.naver.com/")
            .get()

        // 1. 실제 뉴스 리스트가 담긴 'ul.list_news' 내부의 'li'만 타겟팅
        val newsRows = doc.select("ul.list_news > li.bx")
        println("Naver: Found ${newsRows.size} actual news rows.")

        newsRows.mapNotNull { row ->
            // 2. 반드시 'a.news_tit'가 있어야 실제 뉴스 기사로 간주
            val titleElement = row.selectFirst("a.news_tit")

            if (titleElement != null) {
                val title = titleElement.text()
                val link = titleElement.attr("abs:href")

                // 요약 정보 (여러 클래스 시도)
                val summaryElement = row.select(".news_dsc, .api_txt_lines, .dsc_txt_wrap").firstOrNull()
                val summary = summaryElement?.text() ?: "요약 정보 없음"

                println("Naver Parsed: $title")
                NewsItem(title, link, summary, name)
            } else {
                null
            }
        }
    } catch (e: Exception) {
        println("Naver Error: ${e.message}")
        emptyList()
    }
}
}
