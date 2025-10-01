package com.example.tiebukuro.Answer;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
    public interface AnRepository extends JpaRepository<AnswerEntity, Long> {
        // postId で回答を取得するメソッドも追加可能
        List<AnswerEntity> findByPostId(Long postId);
    }

