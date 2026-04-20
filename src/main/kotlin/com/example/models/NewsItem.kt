package com.example.models

import kotlinx.serialization.Serializable

@Serializable
data class NewsItem(
    val title: String,
    val link: String,
    val summary: String,
    val source: String // 네이버, 구글 등 출처 표시
)
