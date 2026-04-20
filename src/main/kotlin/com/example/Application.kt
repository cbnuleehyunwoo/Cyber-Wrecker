package com.example

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
    embeddedServer(Netty, port = 8880, host = "0.0.0.0", module = Application::module)
        .start(wait = true)
}

fun Application.module() {
    install(ContentNegotiation) {
        json(Json {
            ignoreUnknownKeys = true
            encodeDefaults = false // 글로벌 설정: null 필드 완전히 제거 (카카오 규격 준수 필수)
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
            try {
                val request = call.receive<com.example.models.KakaoRequest>()
                
                val keyword = request.action.params["sys_text"] 
                    ?: request.action.params["keyword"] 
                    ?: request.userRequest.utterance.trim()
                    .takeIf { it.isNotEmpty() }
                    ?: "최신 뉴스"
                
                println("Processing keyword: $keyword")
                val newsItems = newsService.getNews(keyword)
                
                val response = if (newsItems.isEmpty()) {
                    com.example.models.KakaoResponse(
                        version = "2.0",
                        template = com.example.models.KakaoTemplate(
                            outputs = listOf(
                                com.example.models.KakaoOutput(
                                    simpleText = com.example.models.KakaoSimpleText(text = "'$keyword'에 대한 검색 결과가 없습니다.")
                                )
                            )
                        )
                    )
                } else {
                    val kakaoItems = newsItems.take(5).map { item ->
                        com.example.models.KakaoListItem(
                            title = item.title.take(35), // 35자로 더 엄격하게 제한
                            description = item.summary.take(50),
                            link = com.example.models.KakaoLink(web = item.link)
                        )
                    }

                    com.example.models.KakaoResponse(
                        version = "2.0",
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
                }

                // 디버깅: 보낼 응답을 JSON으로 찍어보기 (이제 null이 정말 없어야 함)
                val responseJson = Json { encodeDefaults = false; prettyPrint = true }.encodeToString(com.example.models.KakaoResponse.serializer(), response)
                println("Sending Response: $responseJson")


                
                call.respond(response)
            } catch (e: Exception) {
                println("Critical Error in /kakao/news: ${e.message}")
                e.printStackTrace()
                // 에러 발생 시 최소한의 텍스트 응답이라도 보냄
                call.respond(mapOf(
                    "version" to "2.0",
                    "template" to mapOf(
                        "outputs" to listOf(
                            mapOf("simpleText" to mapOf("text" to "서버 오류가 발생했습니다: ${e.message}"))
                        )
                    )
                ))
            }
        }
    }
}
