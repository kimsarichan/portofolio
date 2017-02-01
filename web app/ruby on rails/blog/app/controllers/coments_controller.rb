class ComentsController < ApplicationController
	def create
		@article=Article.find(params[:article_id])
		@coment = @article.coment.create(coments_params)
		redirect_to article_path(@article)
	end

	def destroy
		@article=Article.find(params[:article_id])
		@coment =@article.coment.find(params[:id])
		@coment.destroy
		redirect_to article_path(@article)
	end
	private
		def coments_params
			params.require(:coment).permit(:comenter, :body)
		end

end
