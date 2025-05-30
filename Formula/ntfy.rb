# typed: false
# frozen_string_literal: true

# This file was generated by a script. DO NOT EDIT!
class Ntfy < Formula
  desc "Client to interact with an ntfy pub-sub server"
  homepage "https://github.com/binwiederhier/ntfy"
  url "https://api.github.com/repos/binwiederhier/ntfy/tarball/v2.12.0"
  version "2.12.0"
  sha256 "7fb5c43e19a86d69890c5519065a3863efe895a4b698b794fa0d5d9dc60b11f8"
  license "Apache-2.0"

  depends_on "go" => :build

  on_macos do
    if Hardware::CPU.intel?
      def install
        system "mkdir", "-p", "server/docs"
        ldflags = "-X main.version=#{version} -X main.date=#{time.iso8601}"
        system "go", "build", *std_go_args(ldflags: ldflags), "-tags=noserver"
      end
    end

    if Hardware::CPU.arm?
      def install
        system "mkdir", "-p", "server/docs"
        ldflags = "-X main.version=#{version} -X main.date=#{time.iso8601}"
        system "go", "build", *std_go_args(ldflags: ldflags), "-tags=noserver"
      end
    end
  end

  on_linux do
    if Hardware::CPU.arm? && Hardware::CPU.is_64_bit?
      def install
        system "mkdir", "-p", "server/docs"
        ldflags = "-X main.version=#{version} -X main.date=#{time.iso8601}"
        system "go", "build", *std_go_args(ldflags: ldflags), "-tags=noserver"
      end
    end

    if Hardware::CPU.intel?
      def install
        system "mkdir", "-p", "server/docs"
        ldflags = "-X main.version=#{version} -X main.date=#{time.iso8601}"
        system "go", "build", *std_go_args(ldflags: ldflags), "-tags=noserver"
      end
    end
  end
end
