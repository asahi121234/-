package com.example.tiebukuro.Answer;


//get.htmlからの回答の値を詰める
public class AnswerForm {
    private String Aname;
    private String answer;
    private Long postId;   // 投稿IDを保持するフィールド

    //ゲッター
    public String getAname(){
        return Aname;
    }

    public String getAnswer(){
        return answer;
    }

    public Long getPostId(){
        return postId;
    }

    //セッター
    public void setAname(String Aname){
        this.Aname=Aname;
    }


    public void setAnswer(String answer){
        this.answer =answer;
    }

    public void setPostId(Long postId){
        this.postId=postId;
    }
}
