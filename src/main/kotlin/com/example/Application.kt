package com.example

import com.example.providers.NaverNewsProvider
import com.example.services.NewsService
import io.ktor.serialization.kotlinx.json.*
import io.ktor.server.application.*
import io.ktor.server.engine.*
import io.ktor.server.netty.*
import io.ktor.server.plugins.contentnegotiation.*
import io.ktor.server.request.*
import io.ktor.server.response.*
import io.ktor.server.routing.*
import kotlinx.serialization.json.Json

fun main() {
    embeddedServer(Netty, port = 8080, host = "0.0.0.0", module = Application::module)
        .start(wait = true)
}

fun Application.module() {
    install(ContentNegotiation) {
        json(Json {
            prettyPrint = true
            isLenient = true
        })
    }

    // 의존성 주입 (현재는 안정적인 구글 뉴스만 사용)
    val providers = listOf(com.example.providers.GoogleNewsProvider())
    val newsService = NewsService(providers)

    routing {
        get("/news") {
            val keyword = call.parameters["keyword"] ?: return@get call.respondText("Missing keyword")
            val source = call.parameters["source"]
            
            val news = newsService.getNews(keyword, source)
            call.respond(news)
        }

        // 카카오톡 챗봇 스킬 엔드포인트
        post("/kakao/news") {
            val request = call.receive<com.example.models.KakaoRequest>()
            // 오픈빌더에서 설정한 파라미터 명칭 'sys_text' 사용
            val keyword = request.action.params["sys_text"] 
                ?: request.action.params["keyword"] 
                ?: "최신 뉴스"
            
            val newsItems = newsService.getNews(keyword)
            
            val kakaoItems = newsItems.take(5).map { item ->
                com.example.models.KakaoListItem(
                    title = item.title,
                    description = item.summary.take(50) + "...",
                    link = com.example.models.KakaoLink(web = item.link)
                )
            }

            val response = com.example.models.KakaoResponse(
                template = com.example.models.KakaoTemplate(
                    outputs = listOf(
                        com.example.models.KakaoOutput(
                            listCard = com.example.models.KakaoListCard(
                                header = com.example.models.KakaoHeader(title = "'$keyword' 관련 뉴스"),
                                items = kakaoItems
                            )
                        )
                    )
                )
            )
            call.respond(response)
        }
    }
}
