# typed: false
# frozen_string_literal: true

class Pcopy < Formula
  desc "pcopy is a temporary file host, nopaste and clipboard across machines"
  homepage "https://github.com/binwiederhier/pcopy"
  version "0.6.1"
  url "https://github.com/binwiederhier/pcopy.git",
      tag: "v0.6.1",
      revision: "6e81d03512589b1d3051d240fcfc86e54dde8237"
  license "Apache-2.0"
  head "https://github.com/binwiederhier/pcopy.git", branch: "master"

  depends_on "go" => :build

  def install
    ldflags = "-s -w -X main.version=#{version} -X main.date=#{time.iso8601}"
    system "go", "build", *std_go_args(ldflags: ldflags)
  end
end