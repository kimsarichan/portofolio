class Article < ActiveRecord::Base
	has_many :coment, dependent: :destroy
	validates :title , presence: true,
				length: {minimum: 10}
	validates :text , presence: true,
				length: {minimum: 10}
end
