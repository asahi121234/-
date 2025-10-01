package com.example.tiebukuro.Post;


public class PostForm {
    private String name;
    private String question;
    private String text;

    //ゲッター
    public String getName(){
        return name;
    }

    public String getQuestion(){
        return question;
    }

    public String getText(){
        return text;
    }


    //セッター
    public void setName(String name){
        this.name=name;
    }

    public void setQuestion(String question){
        this.question=question;
    }

    public void setText(String text){
        this.text=text;
    }
}