# GroupMe Tool
# Created on Aug 8, 2017
# @author: Reid Schendel

import requests

auth_token = "auth_token"  # put your auth token here in double quotes
currentGM = -1  # The group chat ID you want to analyze here


def get_member_list(group_id, message_id, member_list):
	"""
	Gets the member list and adds up all like counts.
	"""
	if message_id == 0:
		message_id = get_most_recent_messsage_id(group_id)

	response = requests.get('https://api.groupme.com/v3/groups/' + str(group_id) + '/messages?token=' +
	                        auth_token + '&before_id=' + str(message_id) + '&limit=100')
	data = response.json()

	# see if member is in member_list
	i = 0
	while i < len(data['response']['messages']):
		# print str(data['response']['messages'][i]['user_id'])
		if is_in_list(data['response']['messages'][i]['user_id'], member_list):
			add_to_member(data['response']['messages'][i]['user_id'],
			              member_list,
			              len(data['response']['messages'][i]['favorited_by']))

		# Add new member to list
		else:
			try:
				member = {'name'       : str(data['response']['messages'][i]['name']),
				          'id'         : data['response']['messages'][i]['user_id'],
				          'total_likes': len(data['response']['messages'][i]['favorited_by']),
				          'total_posts': 1}
				print(member)
			except UnicodeEncodeError:  # Jovan exception - For anyone with a non Unicode character in their name.
				member = {'name'       : 'Non-Unicode Character In Name',
				          'id'         : data['response']['messages'][i]['user_id'],
				          'total_likes': len(data['response']['messages'][i]['favorited_by']),
				          'total_posts': 1}

			member_list.append(member)
		i += 1
	# recurse
	last_id = data['response']['messages'][i - 1]['id']
	try:
		get_member_list(group_id, last_id, member_list)
	except ValueError:
		print('Should be done')


def is_in_list(user_id, member_list):
	"""
	Checks if a member is in a list. Returns true if they are, returns false otherwise.
	"""
	i = 0
	while i < len(member_list):
		if user_id == member_list[i]['id']:
			return True
		i += 1
	return False


def add_to_member(user_id, member_list, count):
	"""
	Adds to the member's like count
	"""
	i = 0
	while i < len(member_list):
		if user_id == member_list[i]['id']:
			member_list[i]['total_likes'] += count
			member_list[i]['total_posts'] += 1
			return
		i += 1


def get_most_recent_messsage_id(group_id):
	"""
	Gets the most recent message ID
	"""
	response = requests.get('https://api.groupme.com/v3/groups/' + str(group_id) + '?token=' + auth_token)
	data = response.json()

	return data['response']['messages']['last_message_id']


def get_info(group_name):
	"""
	Gets information on the group ID you specify.
	Goes through all messages, finds all the people who have posted, adds them to a list.
	"""
	response = requests.get('https://api.groupme.com/v3/groups?token=' + auth_token)
	data = response.json()

	if len(data['response']) == 0:
		print("You are not part of any groups.")
		return
	for i in range(len(data['response'])):
		group = data['response'][i]['name']

		if group == group_name:
			print('Returning group id: ', data['response'][i]['name'], data['response'][i]['id'])
			return data

	print("Returning non-specified.")
	return data


def main():

	mem_list = []
	get_member_list(currentGM, 0, mem_list)
	high_list = []

	# Uncomment the code below to run on a groupchat and display the posters with less than 10,000 likes.

	i = 100000
	while i > 0:
		j = 0
		while j < len(mem_list):
			if mem_list[j]['total_likes'] == i:
				high_list.append(mem_list[j])
			j += 1
		i -= 1

	i = 0
	while i < len(high_list):
		ratio = float(float(high_list[i]['total_likes']) / float(high_list[i]['total_posts']))
		print(high_list[i]['name'] + ', Total likes: ' + str(high_list[i]['total_likes']) + ', Total posts: ' + str(
			high_list[i]['total_posts']) + ', Average likes per post: ' + str(ratio))
		i += 1

	get_info(currentGM)


if __name__ == "__main__":
	main()
