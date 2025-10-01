package com.example.tiebukuro.HTMLController;


import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
//get.htmlからpost.htmlへ戻るためのクラス


    @Controller
    public class GetPostController {
        //get.htmlの <a th:href="@{/post}">戻る</a>　をおすとpost.htmlに戻る
        @GetMapping("/post")
        public String post(){
            return "post";
        }

    }


