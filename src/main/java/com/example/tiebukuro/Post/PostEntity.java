package com.example.tiebukuro.Post;

import jakarta.persistence.*;

import java.time.LocalDateTime;


@Entity     //entityの宣言
@Table(name = "posts")  //紐付けるDBテーブル名
public class PostEntity {


    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id; //自動で連番つける

    @Column(nullable = false)  //@ColumnはDBのカラムだよの宣言　（）内の意味はNOT NULLと同じ意味、空の値は入らない
    private String name;       //投稿者の名前を保存するフィールド

    private String text;      //タイトルを保存するフィールド

    @Column(nullable = false,columnDefinition = "TEXT")//NOt NULLと同じで空の値は入らない、columnDefinition = "TEXT"は長い文字列を保存可能
    private String question;   //投稿内容を保存するフィールド

    @Column(name = "created_at",columnDefinition = "TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
    private LocalDateTime createdAt = LocalDateTime.now(); //日時を設定する


    // getter
    public Long getId() { return id; }
    public String getName() { return name; }
    public String getText() { return text; }
    public String getQuestion() { return question; }
    public LocalDateTime getCreatedAt() { return createdAt; }

    // setter
    public void setId(Long id) { this.id = id; }
    public void setName(String name) { this.name = name; }
    public void setText(String text) { this.text = text; }
    public void setQuestion(String question) { this.question = question; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
}



//DBのテーブルと対応するクラスがENTITYクラス
//RipositoryはENTITYのデータを保存、取得、削除するのに役割がある。

