package com.example.tiebukuro.Answer;


import jakarta.persistence.*;

import java.time.LocalDateTime;

@Entity
@Table(name = "answers") //紐づけるテーブル名
public class AnswerEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id; //自動で連番つける

    @Column(name = "post_id", nullable = false)
    private Long postId;  // どの投稿に対する回答か

    @Column(nullable = false)  //@ColumnはDBのカラムだよの宣言　（）内の意味はNOT NULLと同じ意味、空の値は入らない
    private String Aname;       //投稿者の名前を保存するフィールド

    @Column(nullable = false,columnDefinition = "TEXT")//NOt NULLと同じで空の値は入らない、columnDefinition = "TEXT"は長い文字列を保存可能
    private String answer;   //投稿内容を保存するフィールド

    @Column(name = "created_at",columnDefinition = "TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
    private LocalDateTime createdAt = LocalDateTime.now(); //日時を設定する


    // getter
    public Long getId() { return id; }
    public Long getPostId() { return postId; }
    public String getAname(){ return Aname; }
    public String getAnswer(){ return answer; }
    public LocalDateTime getCreatedAt() { return createdAt; }

    // setter
    public void setId(Long id) { this.id = id; }
    public void setPostId(Long postId) { this.postId = postId; }
    public void setAname(String Aname) { this.Aname = Aname; }
    public void setAnswer(String answer) { this.answer = answer; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }


}
