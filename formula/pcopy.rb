# typed: false
# frozen_string_literal: true

# This file was manually edited.
class Pcopy < Formula
  desc "Client to interact with a pcopy temporary file host"
  homepage "https://github.com/binwiederhier/pcopy"
  url "https://github.com/binwiederhier/pcopy.git", revision: "6e81d03512589b1d3051d240fcfc86e54dde8237"
  version "0.6.1"
  license "Apache-2.0"
  head "https://github.com/binwiederhier/pcopy.git", branch: "master"

  depends_on "go" => :build

  def install
    ldflags = "-s -w -X main.version=#{version} -X main.date=#{time.iso8601}"
    system "go", "build", *std_go_args(ldflags: ldflags)
  end
end
