from django.core.paginator import Paginator
from django.conf import settings
from .models import Post


class PostClass():
    def __init__(self, request) -> None:
        self.request = request


    def get_all_posts(self) -> list:
        return Post.objects.all()


    def post_create(self, form) -> object:
        post = form.save(commit=False)
        post.user_ip = self.request.META.get('REMOTE_ADDR')
        post.user_agent_info = self.request.META.get('HTTP_USER_AGENT')
        post.save()

        return post


    def post_detail(self, post, sorting_symbols, comments_sort_options) -> dict:
        context = dict()

        self.__sort_order_defining(sorting_symbols)

        self.__sort_option_defining(post, comments_sort_options, sorting_symbols)

        for key, value in sorting_symbols.items():
            if value.get('default'):
                context.setdefault('sort_order', value)

        if self.page_obj.has_next() or self.page_obj.has_previous():
            context.setdefault('page_obj', self.page_obj)

        context.setdefault('comments', self.comments)
        context.setdefault('post', post)
        context.setdefault('sort_options', comments_sort_options)

        return context 


    def post_comment_create(self, post, form) -> None:
        comment = form.save(commit=False)
        comment.post = post
        comment.user_ip = self.request.META.get('REMOTE_ADDR')
        comment.user_agent_info = self.request.META.get('HTTP_USER_AGENT')
        comment.save()


    def post_comment_to_comment_create(self, pk, post, form, comm, comm_sub) -> None:
        comment = form.save(commit=False)
        comment.post = post
        comment.user_ip = self.request.META.get('REMOTE_ADDR')
        comment.user_agent_info = self.request.META.get('HTTP_USER_AGENT')
        comment.related_to_comment_id = comm
        comment.children_comments = Post.objects.get(id=pk).comments.get(id=comm_sub)
        comment.save()


    def __sort_order_defining(self, sorting_symbols) -> None:
        for key, value in sorting_symbols.items():
            if value.get('default'):
                self.default_sort_db = value.get('db_value')

        if self.request.GET.get('sort_order'):
            for key, value in sorting_symbols.items():
                if value.get('default'):
                    value['default'] = False
            sorting_symbols[self.request.GET.get('sort_order')]['default'] = True
            self.default_sort_db = sorting_symbols.get(self.request.GET.get('sort_order')).get('db_value')

    
    def __sort_option_defining(self, post, comments_sort_options, sorting_symbols) -> None:
        if self.request.GET.get('sort_option'):
            for key, value in comments_sort_options.items():
                if value.get('selected'):
                    value['selected'] = False
            comments_sort_options[self.request.GET.get('sort_option')]['selected'] = True

            self.comments = post.comments.filter(related_to_comment_id=0).order_by(f"{self.default_sort_db}{self.request.GET.get('sort_option')}")
        else:
            for key, value in sorting_symbols.items():
                if value.get('default'):
                    self.comments = post.comments.filter(related_to_comment_id=0).order_by(f"{value.get('db_value')}created_at")
                    
        paginator = Paginator(self.comments, settings.DEFAULT_COMMENTS_PAGINATION)

        page_number = self.request.GET.get('page')
        self.page_obj = paginator.get_page(page_number)


class CommentClass():
    @staticmethod
    def user_and_title_defining(pk, comm, comm_sub) -> tuple:
        if not comm_sub:
            user = Post.objects.get(id=pk).comments.get(id=comm).user_name
            comment_title = Post.objects.get(id=pk).comments.get(id=comm).title
        else:
            user = Post.objects.get(id=pk).comments.get(id=comm_sub).user_name
            comment_title = Post.objects.get(id=pk).comments.get(id=comm_sub).title

        return user, comment_title
