package com.example.models

import kotlinx.serialization.Serializable

@Serializable
data class KakaoRequest(
    val action: Action
)

@Serializable
data class Action(
    val params: Map<String, String>
)

@Serializable
data class KakaoResponse(
    val version: String = "2.0",
    val template: KakaoTemplate
)

@Serializable
data class KakaoTemplate(
    val outputs: List<KakaoOutput>
)

@Serializable
data class KakaoOutput(
    val listCard: KakaoListCard? = null
)

@Serializable
data class KakaoListCard(
    val header: KakaoHeader,
    val items: List<KakaoListItem>,
    val buttons: List<KakaoButton>? = null
)

@Serializable
data class KakaoHeader(
    val title: String
)

@Serializable
data class KakaoListItem(
    val title: String,
    val description: String? = null,
    val link: KakaoLink? = null
)

@Serializable
data class KakaoLink(
    val web: String
)

@Serializable
data class KakaoButton(
    val label: String,
    val action: String,
    val webLinkUrl: String? = null
)
