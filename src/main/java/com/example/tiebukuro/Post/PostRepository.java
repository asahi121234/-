package com.example.tiebukuro.Post;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;


@Repository
public interface PostRepository extends JpaRepository<PostEntity,Long>{

    // 最新10件をID降順で取得
    List<PostEntity>findTop10ByOrderByIdDesc();

    //タイトルor質問文を含む投稿を探す（検索機能）
    List<PostEntity>findByTextContainingOrQuestionContaining(String text, String question);
}

//DBに保存、更新、削除、検索はRepositoryが行う
//interface PostRepositoryはインターフェースだから勝手にデータの取得や保存してくれる
