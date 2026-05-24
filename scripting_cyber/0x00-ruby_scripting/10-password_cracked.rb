#!/usr/bin/env ruby

require 'digest'

if ARGV.length != 2
  puts "Usage: 10-password_cracked.rb HASHED_PASSWORD DICTIONARY_FILE"
  exit 1
end

target_hash = ARGV[0].strip.downcase
dictionary_file = ARGV[1]

begin
  File.foreach(dictionary_file, chomp: true) do |word|
    next if word.nil? || word.empty?

    if Digest::SHA256.hexdigest(word) == target_hash
      puts "Password found: #{word}"
      exit 0
    end
  end

  puts "Password not found in dictionary."

rescue Errno::ENOENT, Errno::EACCES => e
  puts "Error: #{e.message}"
  exit 1
end
