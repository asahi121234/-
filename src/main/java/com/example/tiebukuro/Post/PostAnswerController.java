package com.example.tiebukuro.Post;


import java.util.List;
import com.example.tiebukuro.Answer.AnswerEntity;
import com.example.tiebukuro.Answer.AnswerForm;
import com.example.tiebukuro.Answer.AnRepository;


import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;



//投稿に対してのコントローラクラス
@Controller
public class PostAnswerController {

 @Autowired  //DB操作用のリポジトリを自動で入れる
  private PostRepository postRepository;


 @Autowired
 private AnRepository answerRepository;


    //HTMLから値の受け取り
    @PostMapping("/send")
        public String Post(@ModelAttribute PostForm postForm, Model model) {

        //PostFormから受け取った値をEntityに詰める
        PostEntity post=new PostEntity();
        post.setName(postForm.getName());
        post.setText(postForm.getText());
        post.setQuestion(postForm.getQuestion());

        //DBに保存
        postRepository.save(post);


        // 保存した post をモデルに追加
        model.addAttribute("post", post);

        return "get";//値を返すHTMLファイル
    }


   //Answerの値受け取り(回答の値）
    @PostMapping("/answer")
    public String Anser(@ModelAttribute AnswerForm answerForm, Model model) {

        //AnswerFormから受け取った値をEntityに詰める
        AnswerEntity answer = new AnswerEntity();
        answer.setAname(answerForm.getAname());
        answer.setAnswer(answerForm.getAnswer());
        answer.setPostId(answerForm.getPostId());

        //DBに保存
        answerRepository.save(answer);

       // 投稿をDBから取得
        PostEntity post = postRepository.findById(answerForm.getPostId())
                .orElse(new PostEntity());
        model.addAttribute("post",post);

        //回答一覧をDBから取り出す（投稿に対して紐づいてる回答を全てDBから取り出す）（回答の上書き防止的な）
        List<AnswerEntity> answers = answerRepository.findByPostId(answerForm.getPostId());
        model.addAttribute("answers",answers);


            return "redirect:/get/" + answerForm.getPostId(); //値を返すHTMLファイル（リダイレクトすることで、投稿が二重に表示されなくなる）


    }



        @GetMapping("/get/{id}")
        public String getPost(@PathVariable Long id, Model model){                       //{id}のとこにidを入れる（投稿にはidが割り当てられてる
            PostEntity post = postRepository.findById(id).orElse(new PostEntity());      //DBのテーブルからidと一致する投稿を探して、見つかれば投稿データをpostする。なければ空のPostEntityを作る（エラー回避のため）
            model.addAttribute("post", post);                               //取り出した投稿データをpostの名前でHTMLに渡す。HTMLでは${post.name}みたいに取り出せるようになってる

            List<AnswerEntity> answers = answerRepository.findByPostId(id);           //投稿idに紐づいた回答を全部DBから取り出す。answersというリストに入る
            model.addAttribute("answers",answers);                       //回答一覧をanswersの名前でHTMLに渡す。　htmlではth:each="ans : ${answers}"　でループ表示できる

            return "get";
        }


        //投稿のタイトル一覧１０件をindex.htmlに表示する
    @GetMapping("/")
    public String index(Model model){
        List<PostEntity> posts = postRepository.findTop10ByOrderByIdDesc();//DBから最新の投稿１０件を取り出す　　Repository = データベースとのやり取りのルールを書く場所　　Controller = データを取り出して画面に渡す場所

        model.addAttribute("posts",posts);//posts という名前でHTMLに渡す
        return "index";
    }


     //検索機能
    @GetMapping("/search")
    public String search(@RequestParam("keyword") String keyword,Model model){                                  //@RequestParam("keyword") String keywordは検索したワード（値）を受け取る部分
        List<PostEntity> posts = postRepository.findByTextContainingOrQuestionContaining(keyword,keyword);      //PostEntityのtextカラムかquestionカラムにkeywordが含まれているデータを探してリストで返してくれる
        model.addAttribute("posts",posts);
        model.addAttribute("keyword",keyword);
     return "index";
    }
}
